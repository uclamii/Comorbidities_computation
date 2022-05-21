# installing package
# install only once
# install.packages("comorbidity")

# load the comorbidity package
library(comorbidity)
## This is {comorbidity} version 1.0.2.
## A lot has changed since the last release on CRAN, please check-out breaking changes here:
## -> https://ellessenne.github.io/comorbidity/articles/C-changes.html

compute_charlson_icd9 <- function(x){
  #' Preprocessing df to filter country
  #'
  #' This function returns a subset of the df
  #' if the value of the country column contains 
  #' the country we are passing
  #'
  #
  charlson <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "charlson_icd9_quan", assign0 = FALSE)
  return(charlson)
}

compute_charlson_icd10 <- function(x){
  #' Preprocessing df to filter country
  #'
  #' This function returns a subset of the df
  #' if the value of the country column contains 
  #' the country we are passing
  #'
  #
  charlson <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "charlson_icd10_quan", assign0 = FALSE)
  return(charlson)
}


compute_elixhauser_icd9 <- function(x){
  #' Preprocessing df to filter country
  #'
  #' This function returns a subset of the df
  #' if the value of the country column contains 
  #' the country we are passing
  #'
  #
  elixhauser <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "elixhauser_icd9_quan", assign0 = FALSE)
  return(elixhauser)
}

compute_elixhauser_icd10 <- function(x){
  #' Preprocessing df to filter country
  #'
  #' This function returns a subset of the df
  #' if the value of the country column contains 
  #' the country we are passing
  #'
  #
  elixhauser <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "elixhauser_icd10_quan", assign0 = FALSE)
  return(elixhauser)
}

compute_score<- function(x,map = "charlson_icd10_quan"){
    ### Return it, after adding class 'comorbidity' and some attributes
    class(x) <- c("comorbidity", class(x))
    attr(x = x, which = "map") <- map
    return(score(x = x, weights = NULL, assign0 = FALSE))
}