# Requirements

- **Python version**: 3.7.4  
- **R version**: 3.4.4  
- All other dependencies are specified in `requirements.txt`

# Introduction

This repository computes **Elixhauser** and **Charlson comorbidity scores** at **monthly intervals** using patient diagnosis data. It supports both **ICD-9** and **ICD-10** codes, enabling longitudinal analysis of comorbidity burden over time.

This tool is designed for researchers, data scientists, and healthcare analysts who need to quantify patient comorbidities for modeling or descriptive analytics.

# Getting Started

Follow these steps to get started with the project on your local machine.

## 1. Installation Process

Clone the repository:

```bash
git clone https://github.com/your-username/comorbidity-scoring.git
cd comorbidity-scoring
```


Set up a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## 2. Requirements
For R
```
# installing package
# install only once
# install.packages("comorbidity")
# alternatively
# install.packages("remotes")
# remotes::install_github("ellessenne/comorbidity")
```

For Python 

```
pip install -r requirements.txt
```


## 3.Contribute
We welcome contributions! Here’s how you can help:

- Fork the repository
- Create a new branch for your feature or fix
- Submit a pull request with a clear description of your changes
- Ensure all code is formatted and tested before submission
