import pandas as pd
import numpy as np
from tqdm import tqdm

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def get_comorbidity_df(df, icd_type=10, com_type="charlson"):
    """Method to get the charlson or elixhauser score matrix"""
    # Defining the R script and loading the instance in Python
    r = robjects.r
    r["source"]("comorbidity.R")
    # Loading the function we have defined in R.
    compute_function_r = robjects.globalenv[
        "compute_" + com_type + "_icd" + str(icd_type)
    ]

    # converting it into r object for passing into r function
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df_r = robjects.conversion.py2rpy(df)

    # Invoking the R function and getting the result
    df_result_r = compute_function_r(df_r)

    # Converting it back to a pandas dataframe.
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df_result = robjects.conversion.rpy2py(df_result_r)

    return df_result


def combine_comorbidity_dfs(df1, df2):
    """Method to add 2 dfs by patientid"""
    cols = [col for col in df1.columns]
    len_cols = len(cols) - 1  # -1 for patient id

    df1_df2 = pd.merge(df1, df2, on="patient_id", how="outer").fillna(0)
    patient_ids = df1_df2["patient_id"].values

    # adding the 2 com matrices
    df_values = np.hstack(
        (
            patient_ids.reshape(-1, 1),
            df1_df2.iloc[:, 1 : len_cols + 1].values
            + df1_df2.iloc[:, len_cols + 1 :].values,
        )
    ).astype(int)

    return pd.DataFrame(data=df_values, columns=cols)


def get_combined_comorbidity_df(
    df_dx,
    icd_type_col="icd_type",
    com_type="charlson",
    cols_comorbidities=["patient_id", "icd_code"],
):
    """Method to get combined comorbidity matrix icd9 and icd10"""

    # Reading and processing data
    df_icd9 = df_dx.loc[df_dx[icd_type_col] == 9, cols_comorbidities].reset_index(
        drop=True
    )
    df_icd10 = df_dx.loc[df_dx[icd_type_col] == 10, cols_comorbidities].reset_index(
        drop=True
    )

    df_charlson_icd9 = get_comorbidity_df(df_icd9, icd_type=9, com_type=com_type)
    df_charlson_icd10 = get_comorbidity_df(df_icd10, icd_type=10, com_type=com_type)

    return combine_comorbidity_dfs(df_charlson_icd9, df_charlson_icd10)


def get_score(df):
    """Method to get the charlson or elixhauser score from matrix"""
    # Defining the R script and loading the instance in Python
    r = robjects.r
    r["source"]("comorbidity.R")
    # Loading the function we have defined in R.
    compute_function_r = robjects.globalenv["compute_score"]

    # converting it into r object for passing into r function
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df_r = robjects.conversion.py2rpy(df)

    # Invoking the R function and getting the result
    df_result_r = compute_function_r(df_r)

    # Converting it back to a pandas dataframe.
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df_result = robjects.conversion.rpy2py(df_result_r)

    return df_result


if __name__ == "__main__":

    path = "Data/aki_diags_for_patients_having_cr_lab.csv"

    # # import datasets
    df_dx = pd.read_csv(path, nrows=100)
    df_dx.index = df_dx["diagnosis_datetime"]

    df_charlson = get_combined_comorbidity_df(
        df_dx,
        icd_type_col="icd_type",
        com_type="charlson",
        cols_comorbidities=["patient_id", "icd_code"],
    )

    print(get_score(df=df_charlson))
