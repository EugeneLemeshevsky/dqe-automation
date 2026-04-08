import pytest
import re
import pandas as pd


def test_file_not_empty(csv_data):
    assert len(csv_data) > 0, "CSV file is empty"


@pytest.mark.validate_csv
@pytest.mark.xfail
def test_duplicates(csv_data):
    duplicate_rows = csv_data[csv_data.duplicated()]
    assert len(duplicate_rows) == 0, f"Duplicate rows found: {duplicate_rows}"


@pytest.mark.validate_csv
def test_validate_schema(csv_data, validate_schema):
    expected_columns = ["id", "name", "age", "email", "is_active"]
    validate_schema(actual_schema=csv_data.columns, expected_schema=expected_columns)


@pytest.mark.validate_csv
@pytest.mark.skip
def test_age_column_valid(csv_data):
    for age in csv_data["age"]:
        assert 0 <= age <= 100, f"Invalid age found: {age}"

@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    for email in csv_data["email"]:
        assert re.match(pattern, email), f"Invalid email found: {email}"

@pytest.mark.validate_csv
@pytest.mark.parametrize("user_id, is_active", [(1, False), (2, True)])
def test_active_player(csv_data, user_id, is_active):
    row = csv_data[csv_data["id"] == user_id]
    actual_is_active = row["is_active"].values[0]
    assert actual_is_active == is_active
    
@pytest.mark.validate_csv
def test_active_player_id2(csv_data):
    user_id = 2
    expected_is_active = True
    row = csv_data[csv_data["id"] == user_id]
    actual_is_active = row["is_active"].values[0]
    assert actual_is_active == expected_is_active
