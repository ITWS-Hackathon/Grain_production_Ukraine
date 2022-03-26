library(tidyverse)
library(readxl)
library(dplyr)

#Loading in the dataset
dataset <- read_csv("psd_graines_Ukraine.csv")
head(dataset)
# view(dataset)

#filtering for yield in millions of tons
df <- dataset %>% filter(Unit_Description == "(1000 MT)") #%>%
  # filter(Attribute_Description == "Yield")