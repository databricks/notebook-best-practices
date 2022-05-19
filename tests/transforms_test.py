# Test each of the transform functions.
import pytest
from textwrap import fill
import os
import pandas as pd
import numpy as np
from covid_analysis.transforms import *
from pyspark.sql import SparkSession


@pytest.fixture
def raw_input_df() -> pd.DataFrame:
    """
    Create a basic version of the input dataset for testing, including NaNs.
    """
    df = pd.DataFrame(
        data=[
            ["United States", "USA", "2022-04-17", "Daily ICU occupancy", np.nan],
            [
                "United States",
                "USA",
                "2022-04-17",
                "Daily ICU occupancy per million",
                "4.1",
            ],
            ["United States", "USA", "2022-04-17", "Daily hospital occupancy", "10000"],
            [
                "United States",
                "USA",
                "2022-04-17",
                "Daily hospital occupancy per million",
                "30.3",
            ],
            [
                "United States",
                "USA",
                "2022-04-17",
                "Weekly new hospital admissions",
                "11000",
            ],
            [
                "United States",
                "USA",
                "2022-04-17",
                "Weekly new hospital admissions per million",
                "32.8",
            ],
            ["Algeria", "DZA", "2022-04-18", "Daily ICU occupancy", "1010"],
            ["Algeria", "DZA", "2022-04-18", "Daily ICU occupancy per million", "4.5"],
            ["Algeria", "DZA", "2022-04-18", "Daily hospital occupancy", "11000"],
            [
                "Algeria",
                "DZA",
                "2022-04-18",
                "Daily hospital occupancy per million",
                "30.9",
            ],
            ["Algeria", "DZA", "2022-04-18", "Weekly new hospital admissions", "10000"],
            [
                "Algeria",
                "DZA",
                "2022-04-18",
                "Weekly new hospital admissions per million",
                "32.1",
            ],
        ],
        columns=["entity", "iso_code", "date", "indicator", "value"],
    )

    return df


@pytest.fixture
def colnames_df() -> pd.DataFrame:
    df = pd.DataFrame(
        data=[[0, 1, 2, 3, 4, 5]],
        columns=[
            "Daily ICU occupancy",
            "Daily ICU occupancy per million",
            "Daily hospital occupancy",
            "Daily hospital occupancy per million",
            "Weekly new hospital admissions",
            "Weekly new hospital admissions per million",
        ],
    )
    return df


# Make sure the filter works as expected.
def test_filter(raw_input_df):
    filtered = filter_country(raw_input_df)
    assert filtered.iso_code.drop_duplicates()[0] == "USA"


# The test data has NaNs for Daily ICU occupancy; this should get filled to 0.
def test_pivot(raw_input_df):
    pivoted = pivot_and_clean(raw_input_df, 0)
    assert pivoted["Daily ICU occupancy"][0] == 0


# Test column cleaning.
def test_clean_cols(colnames_df):
    cleaned = clean_spark_cols(colnames_df)
    cols_w_spaces = cleaned.filter(regex=(" "))
    assert cols_w_spaces.empty == True


# Test column creation from index.
def test_index_to_col(raw_input_df):
    raw_input_df["col_from_index"] = raw_input_df.index
    assert (raw_input_df.index == raw_input_df.col_from_index).all()
