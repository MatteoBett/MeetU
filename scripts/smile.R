# Load required libraries
library(fmcsR)
library(igraph)
#library(furrr)
#library(purrr)
library(ChemmineR)
library(ChemmineOB)
#plan(multicore, workers = 12)

get_querry <- function(inchikeys){
    inchikey_query <- pubchemInchikey2sdf(inchikeys)
    # successful queries ?
    set = inchikey_query$sdf_set[inchikey_query$sdf_index != 0]
    return(set)
}


get_neighborhood <- function(ligand){
    # Search using fingreprints
    job1 <- launchCMTool(
        "PubChem Fingerprint Search", # nolint: indentation_linter.
        ligand,
        "Similarity Cutoff" = "0.7",
        "Max Compounds Returned" = "200"
    )   
    result1 <- ChemmineR::result(job1)

    # Get SDFs
    job2 <- launchCMTool("pubchemID2SDF", result1)
    result2 <- ChemmineR::result(job2)
    return(SDFset(append(ligand@SDF,result2@SDF)))
}

compute_graph <- function(ligands, similarity, threshold, n_turnes) {
    n_ligands <- length(ligands@SDF)
    # Create a boolean matrix to track which pairs have been computed
    is_computed <- matrix(FALSE, nrow=n_ligands, ncol=n_ligands)
    # Diagonal is always computed (self-similarity)
    diag(is_computed) <- TRUE
    
    graph <- make_empty_graph()
    graph <- add_vertices(graph, 1, id=1)
    
    for (k in 1:n_turnes) {
        print(paste("turn", k))
        len <- length(V(graph))
        for (i in seq_along(ligands@SDF)) {
            if (!(i %in% V(graph)$id)) {
                test_node <- ligands[[i]]
                
                for (id_j in 1:len) {
                    j = V(graph)$id[id_j]
                    if (!is_computed[i, j]) {
                        t1 <- as.integer(as.POSIXct(Sys.time()))
                        s <- similarity(test_node, ligands[[j]])
                        t2 <- as.integer(as.POSIXct(Sys.time()))
                        if(t2 - t1 > 50){
                            return(make_empty_graph())
                        }
                        is_computed[i, j] <- TRUE
                        is_computed[j, i] <- TRUE
                        
                        if (s > threshold) {
                            print(paste("adding edge", i, j,id_j,len, length(V(graph))))
                            graph <- add_vertices(graph, 1, id=i)
                            graph <- add_edges(graph, edges = c(id_j, length(V(graph))), 
                                            similarity = s)

                            break
                        }
                    }
                }
            }
        }
    }
    return(graph)
}
smiles_to_inchikey <- function(smiles) {
    # Convert SMILES to mol object
    inchikey <-trimws(convertFormat("SMILES","INCHIKEY",smiles))
    return(inchikey)
}
# inchikeys <- c("FNAVCHAKUCOORS-UHFFFAOYSA-N")

args <- commandArgs(trailingOnly = TRUE)
print(args[1])
print(args[2])
stopifnot(length(args) == 2)    
#smiles_data <- readLines("../inputs.smiles")
smiles_data <- readLines(args[1])
#inchikeys <- sapply(smiles_data, smiles_to_inchikey)

#print(inchikeys)
#ligands <- get_querry(inchikeys)
ligand <- read.SDFset(args[1])[1]
#ligands <- c(ligand)
#for(i in seq_along(ligands)){
    #ligand = ligands[i]
    target <- get_neighborhood(ligand)
    g <- compute_graph(target, function(x1, x2) {
        return(fmcs(x1, x2, au = 2, bu = 1, fast = TRUE)[["Tanimoto_Coefficient"]])
    }, threshold = .4, n_turnes = 1)
    #outputs
    dir.exists(args[2])
    write.SMI(sdf2smiles(target[V(g)$id]),paste(args[2],"/neighborhood.smi",sep=""))
    write_graph(g,paste(args[2],"similarity_graph.graphml",sep=""),format = "graphml")
#}
