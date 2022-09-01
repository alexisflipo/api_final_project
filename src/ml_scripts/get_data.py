import csv
from importlib.resources import read_binary
from os import PathLike
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from joblib import dump
import logging
import pickle

africa = 4
oceania = 3
america = 2
europe = 1
asia = 0

COUNTRY_CODE = {
    "DE": europe,
    "JP": america,
    "GB": europe,
    "HN": america,
    "US": america,
    "HU": europe,
    "NZ": oceania,
    "FR": europe,
    "IN": asia,
    "PK": asia,
    "CN": asia,
    "GR": europe,
    "AE": africa,
    "NL": europe,
    "MX": america,
    "CA": america,
    "AT": europe,
    "NG": africa,
    "ES": europe,
    "PT": europe,
    "DK": europe,
    "HR": america,
    "LU": europe,
    "PL": europe,
    "SG": asia,
    "RO": europe,
    "IQ": africa,
    "BR": america,
    "BE": europe,
    "UA": europe,
    "IL": asia,
    "RU": asia,
    "MT": europe,
    "CL": america,
    "IR": asia,
    "CO": america,
    "MD": europe,
    "KE": africa,
    "SI": europe,
    "CH": asia,
    "VN": asia,
    "AS": oceania,
    "TR": europe,
    "CZ": europe,
    "IT": europe,
    "EE": europe,
    "MY": asia,
    "AU": oceania,
    "IE": europe,
    "PH": asia,
    "BG": europe,
    "HK": asia,
    "RS": europe,
    "PR": america,
    "JE": europe,
    "AR": america,
    "BO": america,
}


def get_data(csv_path: PathLike) -> pd.DataFrame:
    data = pd.read_csv(csv_path, index_col=0)
    return data


def create_df_copy(df: pd.DataFrame) -> pd.DataFrame:
    data_copy = df.copy()
    data_copy = drop_duplicates(data_copy)
    return data_copy


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    data = df.drop_duplicates()
    return data


def encode_employment_and_xp(df: pd.DataFrame) -> pd.DataFrame:
    data = df
    data["xp_encoded"] = data["experience_level"].replace(
        {"EN": 0, "MI": 1, "SE": 2, "EX": 3}
    )
    data["employment_type_encoded"] = data["employment_type"].replace(
        {"PT": 0, "FL": 1, "CT": 2, "FT": 3}
    )
    data["salary_usd_in_thousands(k)"] = data["salary_in_usd"] / 1000
    data = data.drop(["salary_in_usd"], axis=1)
    data["salary_usd_in_thousands(k)"] = data["salary_usd_in_thousands(k)"].astype(
        dtype="int32"
    )
    data = data.drop(data[data["salary_usd_in_thousands(k)"] > 275].index, axis=0)
    data_copy = data[data["employment_type_encoded"] == 3]
    data_copy = data_copy.drop(
        [
            "employment_type_encoded",
            "work_year",
            "experience_level",
            "employment_type",
            "salary_currency",
            "salary",
        ],
        axis=1,
    )
    data_copy = drop_duplicates(data_copy)
    data_copy["company_size_encoded"] = data_copy["company_size"].replace(
        {"S": 0, "M": 1, "L": 2}
    )
    data_copy = data_copy.drop(["company_size"], axis=1)
    return data_copy


def encode_location_features(df: pd.DataFrame) -> pd.DataFrame:
    data_copy = df
    data_copy["company_location_encoded"] = data_copy["company_location"].replace(
        COUNTRY_CODE
    )
    data_copy["employee_residence_encoded"] = data_copy["employee_residence"].replace(
        COUNTRY_CODE
    )
    data_copy["employee_residence_encoded"] = data_copy[
        "employee_residence_encoded"
    ].astype(dtype="int32")
    data_copy = data_copy.drop(["company_location", "employee_residence"], axis=1)
    data_copy = data_copy.drop(["company_location_encoded"], axis=1)
    return data_copy


def remove_minority_values(df: pd.DataFrame):
    data_copy = df
    data_copy = data_copy.drop(
        data_copy[data_copy["employee_residence_encoded"] == "africa"].index, axis=0
    )
    data_copy = data_copy.drop(
        data_copy[data_copy["employee_residence_encoded"] == "oceania"].index, axis=0
    )
    return data_copy


def encode(df: pd.DataFrame) -> pd.DataFrame:
    enc = OneHotEncoder(handle_unknown="ignore")
    encoder_df = pd.DataFrame(
        enc.fit_transform(df[["employee_residence_encoded"]]).toarray()
    )
    final_df = pd.concat(
        [encoder_df.reset_index(drop=True), df.reset_index(drop=True)], axis=1
    )
    final_df = final_df.rename(columns={0: "europe", 1: "america", 2: "asia"}).drop(
        ["employee_residence_encoded"], axis=1
    )
    final_df = final_df.drop([3, 4], axis=1)
    return final_df


def set_x_y(df: pd.DataFrame):
    final_df = df
    y = final_df["salary_usd_in_thousands(k)"]
    X = final_df.drop(["job_title", "salary_usd_in_thousands(k)"], axis=1)
    return X, y


def split_train_test(X: set, y: set):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )
    return X_train, X_test, y_train, y_test


# def set_model_with_grisearch() -> GridSearchCV:
#     params_lasso = {
#         "alpha": np.arange(0.1, 1.0, 0.1),
#         "copy_X": [True, False],
#         "max_iter": np.arange(1000, 30000, 5000),
#         "normalize": [False, True],
#         "positive": [False, True],
#         "precompute": [False, True],
#         "selection": ["cyclic", "random"],
#         "warm_start": [False, True],
#     }
#     lasso_mdl = Lasso(alpha=0.1, random_state=42)
#     grid = GridSearchCV(lasso_mdl, param_grid=params_lasso, cv=5)
#     return grid


def train(X_train: set, y_train: set):
    lasso_model = Lasso(alpha=0.1, random_state=42)
    lasso_model.fit(X_train, y_train)
    return lasso_model


def score_and_predict(best_model, X_test, y_test):
    lasso_best_params = best_model
    score = lasso_best_params.score(X_test, y_test)
    return score


def save_model(lasso_best_params):
    with open('src/ml_scripts/models/lasso_model.sav', 'wb') as f:
        pickle.dump(lasso_best_params, f)

def main():
    df = get_data("src/ml_scripts/data/ds_salaries.csv")
    data_copy = create_df_copy(df)
    data_copy_preprocessed = encode_employment_and_xp(data_copy)
    data_copy_preprocessed = encode_location_features(data_copy_preprocessed)
    data_copy_preprocessed = remove_minority_values(data_copy_preprocessed)
    final_df = encode(data_copy_preprocessed)
    X, y = set_x_y(final_df)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = train(X_train, y_train)
    score = score_and_predict(model, X_test, y_test)
    save_model(model)


if __name__ == "__main__":
    main()
