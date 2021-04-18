using Pkg
empty!(DEPOT_PATH)
push!(DEPOT_PATH,  "$(ARGS[1])/.julia")

using Flux, MLDataPattern, Mill, JsonGrinder, JSON, Setfield
using ExplainMill
using BSON: @save, @load
using Logging

#empty values hack
Mill._make_imputing(x::MaybeHotVector, t::Dense) = Mill.postimputing_dense(t)
Mill._make_imputing(x::MaybeHotMatrix, t::Dense) = Mill.postimputing_dense(t)
Mill._make_imputing(x::NGramMatrix, t::Dense) = Mill.postimputing_dense(t)

#############
# CONSTANTS
#############
REPORT_DIR = "$(ARGS[1])/data"
MODEL_DIR = "$(ARGS[1])/out/models"
SAMPLE_NUMBER = ARGS[2]
TRESHOLD = 0.99

############
# LOGGING 
############
io = open("$MODEL_DIR/../explainer.log", "a+")
logger = SimpleLogger(io)
global_logger(logger)

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

function extractdeletelabels!(samples, labels)
    targets = Dict([label => extract_targets(samples, label) for label in labels])
    foreach(i -> delete!(i, "signatures"), samples)
    targets
end


#MAIN
cd(MODEL_DIR)
models = readdir(MODEL_DIR)
for model in models
    #LOAD DATA  
    @info model
    @load "$model/models/model-$model-final.bson" model
    @load "$model/extractor.bson" extractor
    @load "$model/files.bson" files
    @load "$model/split.bson" train_idx test_idx
    test_idx = test_idx[1:SAMPLE_NUMBER]
    files = files[test_idx]
    samples = map(f -> loadjson("$REPORT_DIR/$f"), files)
    targets = extractdeletelabels!(samples, [model])[model]
    data = JsonGrinder.tmap(extractor, samples)
    set = reduce(catobs, data)
    labelnames = [0, 1]
    soft_model = @set model.m.m = Chain(model.m.m, softmax)

    #positive class
    mask = targets .== 1 
    set = set[mask[:]]
    data = data[mask]
    #correctly classified positive class
    mask = labelnames[Flux.onecold(model(set).data)] .== targets[mask]
    set = set[mask]
    data = data[mask]
    #choose only those where model is sure the most
    mask = ExplainMill.confidencegap(soft_model, set, 2) .> TRESHOLD 
    set = set[mask[:]]
    data = data[mask[:]]

    #EXPLAINING
    clustering = ExplainMill._nocluster
    e = ExplainMill.BanzExplainer()
    masks = map(ds -> ExplainMill.explain(e, ds, model, 2, clustering), data)
    rules = map((ms,ds) -> ExplainMill.e2boolean(ds, ms, extractor), masks, data)

    @save "$model/clustering.bson" clustering
    @save "$model/explainer.bson" e
    @save "$model/explain_data.bson" data
    @save "$model/masks.bson" masks

    open("$model/explanations.json", "w") do f
        JSON.print(f, rules, 2)
    end       
    
end