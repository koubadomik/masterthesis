using EvalMetrics
using Plots; pyplot()
using BSON:@load

SCORES = "./scores"
TARGETS = "./targets"
OUT = "./out"
namesA = []
targetsA = []
scoresA = []

models = readdir(SCORES)
for model in models
    @load "$SCORES/$model" soft
    @load "$TARGETS/$model" t1
    targets = t1
    scores = soft
    name = split(model, ".")[1]
    push!(targetsA, targets)
    push!(scoresA, scores)
    push!(namesA, name)
    tresholds = push!(collect(0:0.1:1), 1.000000000000001) #loaded values are sometimes larger than 1 which harms the plots
    
    prplot(targets, scores, tresholds, title=name, grid=false)
    Plots.savefig("$OUT/$model-pr.pdf")
    rocplot(targets, scores, title=name, grid=false)
    Plots.savefig("$OUT/$model-roc.pdf")
    rocplot(targets, scores, xscale=:log10, title=name, xguide="log(false positive rate)", grid=false)
    Plots.savefig("$OUT/$model-roclog.pdf")
end
