library(tidyverse)
library(dplyr)
library(readxl)
library(glmnet)
library(reshape2)
library(ggplot2)

#Loading in the dataset
dataset_net <- read_excel("net_grain.xlsx")
head(dataset_net)

dataset_land <- read_csv("Ukraine_arableLand_cleanData2.csv", skip = 4)
#view(dataset_land)
names(dataset_land)[names(dataset_land) == 'Indicator Code'] <- 'Market Year'

dataset_psd <- read_csv("psd_graines_Ukraine.csv")
# View(dataset_psd)
dataset_psd <-  dataset_psd %>% filter(Commodity_Description == "Wheat" & 
                      Unit_ID == 26)
dataset_psd <- subset(dataset_psd, select = -c(Commodity_Code,Commodity_Description, 
                                               Country_Code, Calendar_Year, Month, 
                                               Attribute_Description, Unit_ID,
                                               Unit_Description, Attribute_ID) )
names(dataset_psd)[names(dataset_psd) == 'Market_Year'] <- 'Market Year'
dataset_1 <- merge(dataset_land, dataset_net, by = "Market Year")
dataset <- merge(dataset_1, dataset_psd, by = "Market Year")
dataset <- na.omit(dataset)
#Exploratory Data Analysis

#only getting numerical columns for a correlation matrix
num_cols <- unlist(lapply(dataset, is.numeric))  
dataset_num <- dataset[ , num_cols] 
cor(dataset_num)

# producing a graphical version of the correlation matrix
correlation_matrix <- round(cor(dataset_num),2)
melted_matrix <- melt(correlation_matrix)
ggplot(data = melted_matrix, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()

#high level of intercorrelations, might need to do a lasso. 
#seeing distributions
hist(dataset$AG.LND.ARBL.ZS)
hist(dataset$Production)
hist(dataset$Value)
# none of these look like normally distributed. To confirm,
# we can run normality distribution tests. 

qqplot(dataset$AG.LND.ARBL.ZS,dataset$Production)
qqplot(dataset$Market_Year, dataset$Production)
qqplot(dataset$Value, dataset$Production)

shapiro.test(dataset$AG.LND.ARBL.ZS)
# W = 0.83864, p-value = 0.000692
shapiro.test(dataset$`Market Year`)
# W = 0.95806, p-value = 0.3335
shapiro.test(dataset$Value)
# W = 0.97529, p-value = 0.7442

ks.test(dataset$AG.LND.ARBL.ZS, dataset$Production)
# D = 1, p-value = 4.441e-16
# alternative hypothesis: two-sided
ks.test(dataset$`Market Year`, dataset$Production)
# D = 1, p-value = 4.441e-16
# alternative hypothesis: two-sided
ks.test(dataset$Value, dataset$Production)
# D = 1, p-value = 4.441e-16
# alternative hypothesis: two-sided

#determining p-value
names(dataset)[names(dataset) == 'Market Year'] <- 'Market_Year'
names(dataset)[names(dataset) == 'AG.LND.ARBL.ZS'] <- 'Arable_Land'
linreg <- lm(Production ~ Market_Year + Arable_Land + Value,  data = dataset)
summary(linreg)
# p - value is 1.024e-12, null hypothesis does not hold. 
# R^r value is 0.9193, may be a bit higher for lasso regression

# Plotting Cook's distance
plot(cooks.distance(linreg))

AIC(linreg)
#484.6009

# due to a high intercorrelation, we plan to use Lasso Regression
#define response variable
y <- dataset$Production
#define matrix of predictor variables
X <- data.matrix(dataset[, c('Market_Year', 'Arable_Land', 'Value')])

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
# R-squared value
sst <- sum((y - mean(y))^2)
sse <- sum((y_predicted - y)^2)
rsq <- 1 - sse/sst
rsq
# 0.9192103

pred <- data.frame(Market_Year = 2022, Arable_Land = 56.76217, Value = 4.46)
pred <- data.matrix(pred)
y_hat <- predict(best_model, s = best_lambda, newx = pred)
#98% of Ukraine's exports go through their ports


# Ridge regression
ridge_model <- glmnet(X, y, alpha = 0, lambda = best_lambda)
coef(ridge_model)

y_predicted <- predict(ridge_model, s = best_lambda, newx = X)
# R-squared value
sst <- sum((y - mean(y))^2)
sse <- sum((y_predicted - y)^2)
rsq <- 1 - sse/sst
rsq
# 0.9192198