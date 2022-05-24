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

    if (df1[cols[1:]].fillna(0).values > 1).any() or (
        df2[cols[1:]].fillna(0).values > 1
    ).any():
        raise Exception("One of dfs has comorbidities larger than 1")

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

    df = pd.DataFrame(data=df_values, columns=cols)
    df[cols[1:]] = (df[cols[1:]] > 0) * 1
    # according to Theonas suggestion we do not count
    # counts more than 1 in each comorbidity

    return df


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

    if df_icd9.empty and df_icd10.empty:
        raise Exception("Both dfs empty no icd codes")
    elif df_icd9.empty:
        return get_comorbidity_df(df_icd10, icd_type=10, com_type=com_type)
    elif df_icd10.empty:
        return get_comorbidity_df(df_icd9, icd_type=9, com_type=com_type)
    else:
        df_coms_icd9 = get_comorbidity_df(df_icd9, icd_type=9, com_type=com_type)
        df_coms_icd10 = get_comorbidity_df(df_icd10, icd_type=10, com_type=com_type)
        return combine_comorbidity_dfs(df_coms_icd9, df_coms_icd10)


def get_score(df, weight, map="charlson_icd10_quan"):
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
    df_result_r = compute_function_r(df_r, weight, map)

    # Converting it back to a pandas dataframe.
    with localconverter(robjects.default_converter + pandas2ri.converter):
        df_result = robjects.conversion.rpy2py(df_result_r)

    return df_result


if __name__ == "__main__":

    path = "Data/Diagnosis.txt"

    # # import datasets
    df_dx = pd.read_csv(path)  # , nrows=100)
    # changing to lowercase columns
    df_dx.columns = map(str.lower, df_dx.columns)
    df_dx["diagnosis_datetime"] = pd.to_datetime(df_dx["diagnosis_datetime"]).astype(
        str
    )

    df_dx["year_month"] = [val[:7] + "-01" for val in df_dx["diagnosis_datetime"]]

    unique_months = sorted(df_dx.year_month.unique())

    # setting index to dates to slice monthly
    df_dx.index = pd.to_datetime(df_dx["diagnosis_datetime"])

    risk_score_type = "elixhauser"  # elixhauser
    weight_type = "swiss"
    df_risk = pd.DataFrame()
    for iter, month_col in tqdm(enumerate(unique_months[1:])):
        # month_col = unique_months[20]
        df_month_sample = df_dx[:month_col]

        df_coms = get_combined_comorbidity_df(
            df_month_sample,
            icd_type_col="icd_type",
            com_type=risk_score_type,
            cols_comorbidities=["patient_id", "icd_code"],
        )

        pat_ids = df_coms["patient_id"].tolist()
        pat_risk = get_score(
            df=df_coms,
            weight=weight_type,
            map=risk_score_type + "_icd10_quan",
        )
        df_risk_sample = pd.DataFrame(
            data=np.vstack((pat_ids, pat_risk)).T,
            columns=["patient_id", "Risk_" + month_col],
        )

        if iter == 0:
            df_risk = df_risk_sample
        else:
            df_risk = pd.merge(
                df_risk,
                df_risk_sample,
                on="patient_id",
                how="outer",
            ).fillna(0)

    print("Number of patients computed risk over time: ", len(df_risk))

    df_risk.to_csv("Data/" + risk_score_type + "_risk_over_time.csv", index=False)
