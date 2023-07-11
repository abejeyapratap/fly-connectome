
#Must read the following libraries first 
library(neuprintr) ## Only one that is really needed for the script below

#Will need to have a neuprint token and pointing to a server use the following command to set them up
usethis::edit_r_environ()

###Copy and paste the below into your environment (.Renviron file)
neuprint_server="https://neuprint.janelia.org"
neuprint_token="INSERT YOUR TOKEN"
neuprint_dataset= "hemibrain:v1.2.1"

###These are other tools I use for visualization and other potential helpful libraries
#library(natverse)
#library(tidyverse)
#library(catmaid)
#library(hemibrainr)
#library(fafbseg)
#library(reticulate)
#library(elmr)
#library(gargle)
#library(nat.flybrains)
#library(nat.jrcbrains)
#library(nat.nblast)
#library(shiny)
#library(dendroextras)
#library(network)
#library(ggplot2)
#library(network)
#library(ggnetwork)

#Get the DN's ID's

DNp01 = neuprint_ids("Giant Fiber") # ("2307027729")
neuprint_ids("DNp02") # ("5813024015")
neuprint_ids("DNp03") # ("1565846637")
neuprint_ids("DNp04") # ("1405231475")
neuprint_ids("DNp05") # ("1466998977")
neuprint_ids("DNp06") # ("5813023322")
neuprint_ids("DNp07") # ("1100404581")
neuprint_ids("DNp08") # (no valid id)
neuprint_ids("DNp09") # ("1226887763" "1228264951")
neuprint_ids("DNp10") # ("512851433"  "5813026936")
neuprint_ids("DNp11") # ("1281324958")


###This list below can be adapt to pull pre and post partners from any population
DNs <- list("2307027729","5813024015", "1565846637", "1405231475", "5813023322", "1100404581", "1226887763", "1228264951", "512851433", "5813026936","1281324958")

LC4 <- neuprint_ids('LC4')
LC4
LPLC2 <-neuprint_ids("LPLC2")
LPLC2
VPNs <- list(c(LC4, LPLC2))
VPNs

length(LC4)
length(LPLC2)
lengths(VPNs)


## Connectivity inputs to the DN's of interest above this shows the major populations of inputs and outputs
inputs_DNp01 <- neuprint_simple_connectivity(2307027729, prepost = 'PRE')
outputs_DNp01 <- neuprint_simple_connectivity(2307027729, prepost = 'POST')
head(sort(table(inputs_DNp01$type), decreasing = TRUE))
head(sort(table(outputs_DNp01$type), decreasing = TRUE))

inputs_DNp03 <- neuprint_simple_connectivity(1565846637, prepost = 'PRE')
outputs_DNp03 <- neuprint_simple_connectivity(1565846637, prepost = 'POST')
head(sort(table(inputs_DNp03$type), decreasing = TRUE))
head(sort(table(outputs_DNp03$type), decreasing = TRUE))

inputs_DNp06 <- neuprint_simple_connectivity(5813023322, prepost = 'PRE')
outputs_DNp06 <- neuprint_simple_connectivity(5813023322, prepost = 'POST')
head(sort(table(inputs_DNp06$type), decreasing = TRUE))
head(sort(table(outputs_DNp06$type), decreasing = TRUE))

# Trying to get the number of synaptic inputs from a given population (This gives synaptic locations, which you can extract the number of synapses from each given id)
DNp01_syn= neuprint_get_synapses(2307027729)
Dnp03_syn= neuprint_get_synapses(1565846637)
Dnp06_syn=neuprint_get_synapses(5813023322)

### This gets the connections of inputs and outputs of DN's pre and post
Conn_pre=neuprint_connection_table(DNs, partners='inputs', details = TRUE)
Conn_pre
Conn_post=neuprint_connection_table(DNs, partners='outputs', details = TRUE)
Conn_post
Conn_all <- rbind(Conn_pre, Conn_post)


write.csv(Conn_all, "Conn_pre_and_post_DNs.csv")

