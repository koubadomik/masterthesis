using Pkg
empty!(DEPOT_PATH)
push!(DEPOT_PATH,  "$(ARGS[1])/.julia")

using Flux, MLDataPattern, Mill, JsonGrinder, JSON, Statistics, IterTools, LazyJSON, Mmap
using Serialization
using JsonGrinder: suggestextractor, ExtractDict
using Mill: reflectinmodel
using StatsBase: sample
using Random
using BSON: @save, @load
using Logging
using Dates
using EvalMetrics
using PrayTools

#Empty values hack
Mill._make_imputing(x::MaybeHotVector, t::Dense) = Mill.postimputing_dense(t)
Mill._make_imputing(x::MaybeHotMatrix, t::Dense) = Mill.postimputing_dense(t)
Mill._make_imputing(x::NGramMatrix, t::Dense) = Mill.postimputing_dense(t)

#############
# CONSTANTS
#############
SAMPLE_NUMBER = 80_000
NEURONS = 20
REPORT_DIR = "$(ARGS[1])/data"
OUTPUT_DIR = "$(ARGS[1])/out"
MINIBATCH_SIZE = 1000
ITERATIONS = 120
REPORT_PERIOD = 10


############
# LOGGING 
############
io = open("$OUTPUT_DIR/analyser.log", "a+")
logger = SimpleLogger(io)
global_logger(logger)

############
# OUTPUT DIRECTORY
###########
if !isdir("$OUTPUT_DIR/models")
    mkdir("$OUTPUT_DIR/models")
end


############
# FUNCTIONS
############
function loadjson(file)
    json = open(file, "r") do s
        JSON.parse(s)
    end
    return json
end

function extract_targets(samples, signature)
    return map(
        sample -> signature in map(signature -> signature["name"], sample["signatures"]),
        samples,
    )
end

function partitionTrainTest(data, at = 0.5)
    n = length(data)
    idx = shuffle(1:n)
    train_idx = view(idx, 1:floor(Int, at * n))
    test_idx = view(idx, (floor(Int, at * n)+1):n)
    @save "$OUTPUT_DIR/split.bson" train_idx test_idx
    train_idx, test_idx
end

# PIPELINE FUNCTIONS
function loadsamples()
    cd(REPORT_DIR)
    files = readdir()
    files = filter(
        f -> split(f, ".")[2] == "json",
        filter(f -> length(split(f, ".")) != 1, files),
    ) #firstly remove directories, secondly choose only .json files
    files = sample(
        files,
        length(files) > SAMPLE_NUMBER ? SAMPLE_NUMBER : length(files),
        replace = false,
    )
    @save "$OUTPUT_DIR/files.bson" files
    map(f -> loadjson(f), files)
end

function getsignatures(samples)
    sch = JsonGrinder.schema(samples)
    counts = sch[:signatures].items[:name].counts
    sorted = sort(collect(counts), by = x -> x[2])
    @info sorted
    [i[1] for i in sorted]
end

function extractdeletelabels!(samples, labels)
    targets = Dict([label => extract_targets(samples, label) for label in labels])
    foreach(i -> delete!(i, "signatures"), samples)
    targets
end

function getschemaextractor(samples)
    sch = JsonGrinder.schema(samples)
    sch, suggestextractor(sch)
end

function buildmodel(sch, extractor, len)
    @info "BUILDING MODEL"
    model = reflectinmodel(
        sch,
        extractor,
        k -> Dense(k, NEURONS, relu),
        d -> Aggregation(SegmentedMean(d), SegmentedMax(d)),
        fsm = Dict("" => k -> Dense(k, len)),
    )
    ps = Flux.params(model)
    model, ps
end

#DATA
samples = loadsamples()
train_idx, test_idx = partitionTrainTest(samples)
signatures = [ARGS[2]]
targets = extractdeletelabels!(samples, signatures)
labelnames = [0, 1]
sch, extractor = getschemaextractor(samples[train_idx, :])
train_data = JsonGrinder.tmap(extractor, samples[train_idx, :])
test_data = JsonGrinder.tmap(extractor, samples[test_idx, :])
@save "$OUTPUT_DIR/extractor.bson" extractor
@save "$OUTPUT_DIR/schema.bson" sch 
@load "$OUTPUT_DIR/extractor.bson" extractor
@load "$OUTPUT_DIR/schema.bson" sch
 
#TRAIN/TEST LOOP FOR EACH SIGNATURE
for signature in signatures
    @info "DATA"
    label = signature
    @info label
    train_targets = targets[label][train_idx, :]
    test_targets = targets[label][test_idx, :]
    t1 = test_targets[:]
    t2 = train_targets[:]
    @save "$OUTPUT_DIR/test_targets.bson" t1
    @save "$OUTPUT_DIR/train_targets.bson" t2
    trainset = reduce(catobs, train_data)
    testset = reduce(catobs, test_data)
    trn_onehottargets = Flux.onehotbatch(train_targets[:], labelnames)
    tst_onehottargets = Flux.onehotbatch(test_targets[:], labelnames)

    @info "VARIABLES"
    flush(io)
    iter = 0
    opt = ADAM()
    test_lossf, train_lossf, test_accur, train_accur = [], [], [], []
    model, params = buildmodel(sch, extractor, length(labelnames))
    accuracy(x, y) = mean(labelnames[Flux.onecold(model(x).data)] .== y)
    loss = (x, y) -> Flux.Losses.logitcrossentropy(model(x).data, y)
    cb =
        () -> begin
            test_stat = Dict(
                            "bal_acc" =>  balanced_accuracy(test_targets[:], labelnames[Flux.onecold(model(testset).data)]),
                            "f1" => f1_score(test_targets[:], labelnames[Flux.onecold(model(testset).data)]),
                            "fpr" => false_positive_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)]),
                            "fnr" => false_negative_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
                             )
            train_stat = Dict(
                            "bal_acc" =>  balanced_accuracy(train_targets[:], labelnames[Flux.onecold(model(trainset).data)]),
                            "f1" => f1_score(train_targets[:], labelnames[Flux.onecold(model(trainset).data)]),
                            "fpr" => false_positive_rate(train_targets[:], labelnames[Flux.onecold(model(trainset).data)]),
                            "fnr" => false_negative_rate(train_targets[:], labelnames[Flux.onecold(model(trainset).data)])
                            )
            train_acc = accuracy(trainset, train_targets)
            test_acc = accuracy(testset, test_targets)
            train_loss = loss(trainset, trn_onehottargets)
            test_loss = loss(testset, tst_onehottargets)
            push!(train_lossf, train_loss)
            push!(test_lossf, test_loss)
            push!(train_accur, train_acc)
            push!(test_accur, test_acc)
            @info "ITERATION: $iter / $ITERATIONS | TIME: $(round(Dates.datetime2unix(now())-start, digits=3))s | accuracy: train = $train_acc, test = $test_acc | loss: train = $train_loss, test = $test_loss"
            @info "Train stats " train_stat
            @info "Test stats: " test_stat
            if mod(iter, REPORT_PERIOD) == 0
                @save "$OUTPUT_DIR/models/model-$(label)-inter-$(iter).bson" model
                soft = softmax(model(testset).data)[2, :]
                @save "$OUTPUT_DIR/test_scores-$(label)-inter-$(iter).bson" soft
            end
            flush(io)
        end
    minibatch =
        () -> begin
            idx = sample(1:length(train_data), MINIBATCH_SIZE, replace = false)
            iter += 1
            trainset[idx], trn_onehottargets[:, idx]
        end

    @info "TRAINING"
    start = Dates.datetime2unix(now())
    Flux.Optimise.train!(
        loss,
        params,
        repeatedly(minibatch, ITERATIONS),
        opt,
        cb = Flux.throttle(cb, 2),
    )

    @info "TESTING AND EVALUATION"
    #METRICS
    test_accuracy = accuracy(testset, test_targets)
    test_loss = loss(testset, tst_onehottargets)
    confumat = ConfusionMatrix(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    bin_report = binary_eval_report(test_targets[:], softmax(model(testset).data)[2, :])
    bal_acc = balanced_accuracy(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    f1 = f1_score(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    true_positive = true_positive_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    true_negative = true_negative_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    false_positive = false_positive_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    false_negative = false_negative_rate(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    prec = precision(test_targets[:], labelnames[Flux.onecold(model(testset).data)])
    
    #SAVE
    modelfile = "$OUTPUT_DIR/models/model-$(label)-final.bson"
    report = Dict(
        "signature" => label,
        "eval" => Dict(
            "test_accuracy" => test_accuracy,      
            "test_loss" => test_loss,
            "tst_ac" => test_accur,
            "trn_ac" => train_accur,
            "trn_loss" => train_lossf,
            "tst_loss" => test_lossf,
            "confus_matr" => string(confumat),
            "binary_eval" => string(bin_report),
            "balanced_accuracy" => bal_acc,
            "true_positive_rate" => true_positive,
            "true_negative_rate" => true_negative,
            "false_positive_rate" => false_positive,
            "false_negative_rate" => false_negative,
            "precision" => prec,
            "f1_score" => f1
        ),
        "HYPERPARAMS" => Dict(
            "ITERATIONS" => ITERATIONS,
            "NEURONS" => NEURONS,
            "MINIBATCH_SIZE" => MINIBATCH_SIZE,
        ),
        "FILE" => modelfile,
    )

    open("$OUTPUT_DIR/models/models.json", "a") do s
        JSON.print(s, report)
        write(s, "\n")
    end

    summary = Dict(
        "signature" => label,
        "test_accuracy" => test_accuracy,
        "test_loss" => test_loss,
    )

    open("$OUTPUT_DIR/models/summary.json", "a") do s
        JSON.print(s, summary)
        write(s, "\n")
    end

    soft = softmax(model(testset).data)[2, :]
    @save "$OUTPUT_DIR/test_scores-$(label)-final.bson" soft
    @save modelfile model
end