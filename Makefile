.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = CKD_progression
PYTHON_INTERPRETER = python3


ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

date_str = $(shell date +%Y-%m-%d -d "1 days ago")

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Save current requirements
freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

## Preparing race and other demographics
demographics_data:
	$(PYTHON_INTERPRETER) demographics_dataset.py

## Sorting data by PatientID and time-taken
sort_data:
	$(PYTHON_INTERPRETER) sorting_dataset.py

## Changing format of text_results to float (only specific for UCLA)
text_2_float_data:
	$(PYTHON_INTERPRETER) text_2_float_dataset.py

## Estimating baseline data
baseline_data:
	$(PYTHON_INTERPRETER) baseline_estimation.py

## Detecting AKI data
AKI_data:
	$(PYTHON_INTERPRETER) AKI_detection.py

## Pivoting AKI data
AKI_pivot:
	$(PYTHON_INTERPRETER) AKIs_pivot.py

## EGFR data generation
EGFR_data:
	$(PYTHON_INTERPRETER) egfr_estimation.py

## Pivoting egfr data
EGFR_pivot:
	$(PYTHON_INTERPRETER) EGFR_pivot.py

## Conditions data Pivotting
conditions_pivot:
	$(PYTHON_INTERPRETER) conditions_pivot.py

## Centering AKIs and EGFR to conditions first date
center_conditions: center_CKD center_HTN center_PDM center_DM center_DM_md center_DM_lb center_DM_dx

center_CKD:
	$(PYTHON_INTERPRETER) center_condition.py CKD

center_HTN:
	$(PYTHON_INTERPRETER) center_condition.py HTN

center_PDM:
	$(PYTHON_INTERPRETER) center_condition.py PDM

center_DM:
	$(PYTHON_INTERPRETER) center_condition.py DM

center_DM_md:
	$(PYTHON_INTERPRETER) center_condition.py DM_md

center_DM_lb:
	$(PYTHON_INTERPRETER) center_condition.py DM_lb

center_DM_dx:
	$(PYTHON_INTERPRETER) center_condition.py DM_dx

########################################################################
########################################################################
## Sorting ICD code AKIs data by PatientID and time-taken
sort_ICD_code_AKI_data:
	$(PYTHON_INTERPRETER) sorting_ICD_code_AKI_dataset.py

## Pivoting ICD code AKI data
ICD_code_AKI_pivot:
	$(PYTHON_INTERPRETER) ICD_code_AKI_pivot.py

## Evaluating ICD code AKI data vs AKI Sr. Creatinine data
evaluation_AKI_ICD_code_AKI:
	$(PYTHON_INTERPRETER) evaluate_AKIs_ICD_code_AKIs.py

########################################################################
########################################################################

## Preprocess data for dashboard
image:
	docker build -t cure_ckd_dashboard .
