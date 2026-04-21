import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df: pd.DataFrame, column_names: list = None):
        if column_names:
            duplicates = df.duplicated(subset=column_names).sum()
        else:
            duplicates = df.duplicated().sum()
        assert duplicates == 0, f"Found {duplicates} duplicate rows"

    @staticmethod
    def check_count(df1: pd.DataFrame, df2: pd.DataFrame):
        assert len(df1) == len(df2), f"Row count mismatch: {len(df1)} vs {len(df2)}"
        
    @staticmethod
    def check_data_completeness(df1: pd.DataFrame, df2: pd.DataFrame):
        pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

    @staticmethod
    def check_data_full_data_set(df1: pd.DataFrame, df2: pd.DataFrame):
        pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

    @staticmethod
    def check_dataset_is_not_empty(df: pd.DataFrame):
        assert len(df) > 0, "Dataset is empty"

    @staticmethod
    def check_not_null_values(df: pd.DataFrame, column_names: list = None):
        columns = column_names if column_names else df.columns.tolist()
        for col in columns:
            nulls = df[col].isnull().sum()
            assert nulls == 0, f"Column '{col}' has {nulls} null values"
