# installing package
# install only once
# install.packages("comorbidity")
# alternatively
# install.packages("remotes")
# remotes::install_github("ellessenne/comorbidity")

# load the comorbidity package
library(comorbidity)

compute_charlson_icd9 <- function(x){
  #' estimating icd9 comorbidities matrix

  charlson <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "charlson_icd9_quan", assign0 = FALSE)
  return(charlson)
}

compute_charlson_icd10 <- function(x){
  #' Estimating icd10 comorbidities matrix

  charlson <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "charlson_icd10_quan", assign0 = FALSE)
  return(charlson)
}


compute_elixhauser_icd9 <- function(x){
  #' estimating icd9 comorbidities matrix

  elixhauser <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "elixhauser_icd9_quan", assign0 = FALSE)
  return(elixhauser)
}

compute_elixhauser_icd10 <- function(x){
  #' Estimating icd10 comorbidities matrix

  elixhauser <- comorbidity(x = x, id = "patient_id", code = "icd_code", map = "elixhauser_icd10_quan", assign0 = FALSE)
  return(elixhauser)
}

compute_score<- function(x,weight="charlson",map = "charlson_icd10_quan"){
    ### Return it, after adding class 'comorbidity' and some attributes
    class(x) <- c("comorbidity", class(x))
    attr(x = x, which = "map") <- map
    return(score(x = x, weights = weight, assign0 = FALSE))
}