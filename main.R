library(tidyverse)
library(dplyr)
library(readxl)
library(glmnet)

#Loading in the dataset
dataset_net <- read_excel("net_grain.xlsx")
head(dataset_net)

dataset_land <- read_csv("Ukraine_arableLand_cleanData2.csv", skip = 4)
#view(dataset_land)
names(dataset_land)[names(dataset_land) == 'Indicator Code'] <- 'Market Year'

dataset <- merge(dataset_land, dataset_net, by = "Market Year")
dataset <- na.omit(dataset)
#Exploratory Data Analysis

#only getting numerical columns for covariance
num_cols <- unlist(lapply(dataset, is.numeric))  
dataset_num <- dataset[ , num_cols] 
cor(dataset_num)

#high level of intercorrelations, might need to do a lasso. 
#seeing distributions
hist(dataset$AG.LND.ARBL.ZS)
hist(dataset$Production)

#determining p-value
names(dataset)[names(dataset) == 'Market Year'] <- 'Market_Year'
names(dataset)[names(dataset) == 'AG.LND.ARBL.ZS'] <- 'Arable_Land'
linreg <- lm(Production ~ Market_Year + Arable_Land,  data = dataset)
summary(linreg)
# p - value is 0.0003575, null hypothesis does not hold. 

# due to a high intercorrelation, we plan to use Lasso Regression
#define response variable
y <- dataset$Production

#define matrix of predictor variables
X <- data.matrix(dataset[, c('Market_Year', 'Arable_Land')])

#perform k-fold cross-validation to find optimal lambda value
cv_model <- cv.glmnet(X, y, alpha = 1)
#find optimal lambda value that minimizes test MSE
best_lambda <- cv_model$lambda.min
best_lambda
#produce plot of test MSE by lambda value
plot(cv_model) 

best_model <- glmnet(X, y, alpha = 1, lambda = best_lambda)
coef(best_model)

y_predicted <- predict(best_model, s = best_lambda, newx = X)

#find SST and SSE
sst <- sum((y - mean(y))^2)
sse <- sum((y_predicted - y)^2)

#find R-Squared
rsq <- 1 - sse/sst
rsq

#98% of Ukraine's exports go through their ports

