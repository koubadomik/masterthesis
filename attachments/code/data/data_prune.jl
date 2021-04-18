using JsonGrinder, JSON, Statistics, IterTools, LazyJSON, Mmap
using Serialization
using StatsBase: sample
#############
# CONSTANTS
#############
REPORT_DIR = ""
PRUNED_DIR = ""
TOPRUNE = [
           "procdump",
           "strings",
           "ttps",
           "info",
           "dropped",
           "procmemory",
           "malfamily_tag",
           "target",
           "debug",
           "suricata",
           "statistics",
           "deduplicated_shots",
           #"signatures"
           "behavior.processtree",
           "behavior.processes",
           "behavior.encryptedbuffers",
           "behavior.anomaly",
	   "behavior.enhanced",
	   "network",
           "curtain",
           "virustotal",
           "malscore",
           "detections",
           "static",
           "CAPE"
           ]
SAMPLE_NUMBER = 80_000

############
# FUNCTIONS
############
function getlevels(str, del=".")
    spl = split(str, del)
    return (spl[1], spl[2])
end

function prunejson(json, toprune)
    toplevel = filter(t -> !occursin(".", t),toprune)
    secondlevel = filter(t -> occursin(".", t), toprune)
    secondlevel = map(getlevels, secondlevel)
    foreach(attr -> delete!(json, attr),toplevel)
    foreach(attr -> delete!(json[attr[1]], attr[2]), secondlevel)
end


function load_prune_write(file; toprune=TOPRUNE)
    open(file, "r") do s
         try
            if !isfile("$(PRUNED_DIR)/$(file)")
                r = LazyJSON.value(Mmap.mmap(s))
                json = merge(Dict("behavior"=> convert(Dict, r["behavior"]), "signatures"=> convert(Array, r["signatures"])))
                prunejson(json, toprune)
                open("$(PRUNED_DIR)/$(file)", "w") do f
                    JSON.print(f, json)
                end
            else
                println("Skipping file, it is already pruned")
            end
        catch
            print("Not valid json, skipping")
        end
    end
end

function savepruned(files, samples)
    for (i, sample) in enumerate(samples)
        open("$(files[i])", "w") do f
            JSON.print(f, sample)
        end
    end
end


##########
## MAIN ##
##########
# LOAD
cd(REPORT_DIR)
files = readdir()
files = filter(f -> split(f,".")[2] == "json", filter(f -> length(split(f, ".")) != 1, files)) #firstly remove directories, secondly choose only .json files
files = sample(files, length(files) > SAMPLE_NUMBER ? SAMPLE_NUMBER : length(files),replace=false)
#PRUNE AND SAVE
foreach(f -> load_prune_write(f), files)