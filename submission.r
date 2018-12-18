library(igraph)
library(d3Network)

fGraph1 <- read.graph(file = "facebook/0.edges", directed = FALSE)
fGraph1 <- simplify(fGraph1, remove.multiple = TRUE, remove.loops = TRUE)

trans <- transitivity(fGraph1, type = "localaverage",isolates = "zero")
avgPath <- average.path.length(fGraph1)
comBetween <- edge.betweenness.community(fGraph1)

set.seed("20181215")
plot(fGraph1,
     vertex.color = comBetween$membership, vertex.size = log(degree(fGraph1) + 1),
     mark.groups = by(seq_along(comBetween$membership), comBetween$membership, invisible))

title("SNAP Facebook Edge 0")

samples <- c(13,24,57,153)

samplesDF <-
  data.frame(
    degree      = degree(fGraph1),
    betweenness = betweenness(fGraph1),
    closeness   = closeness(fGraph1))

samplesDF[samples,]
