import pandas as pd
import pyarrow.parquet as pq


def read_html_table(table_element):
    columns = table_element.find_elements("class name", "y-column")

    data = {}
    for column in columns:
        header = column.find_element("id", "header").text.strip()
        cells = column.find_elements("class name", "cell-text")

        values = []
        for cell in cells:
            text = cell.text.strip()
            if text != header:
                values.append(text)

        data[header] = values

    df = pd.DataFrame(data)
    return df


def read_parquet(folder, filter_date=None):
    dataset = pq.ParquetDataset(folder)
    df = dataset.read().to_pandas()

    if filter_date:
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
                df = df[df[col] == filter_date]
                break

    return df.reset_index(drop=True)


COLUMN_MAPPING = {
    "Facility Type": "facility_type",
    "Visit Date": "visit_date",
    "Average Time Spent": "avg_time_spent",
}


def compare_dataframes(df_html, df_parquet):
    df_html = df_html.rename(columns=COLUMN_MAPPING)

    common_cols = []
    for col in df_html.columns:
        if col in df_parquet.columns:
            common_cols.append(col)

    df_html = df_html[common_cols].copy()
    df_parquet = df_parquet[common_cols].copy()

    for col in common_cols:
        try:
            df_html[col] = pd.to_numeric(df_html[col]).round(2)
            df_parquet[col] = pd.to_numeric(df_parquet[col]).round(2)
        except (ValueError, TypeError):
            df_html[col] = df_html[col].astype(str).str.strip()
            df_parquet[col] = df_parquet[col].astype(str).str.strip()

    if "visit_date" in common_cols:
        html_dates = df_html["visit_date"].unique()
        df_parquet = df_parquet[df_parquet["visit_date"].isin(html_dates)]

    df_html = df_html.sort_values(by=common_cols).reset_index(drop=True)
    df_parquet = df_parquet.sort_values(by=common_cols).reset_index(drop=True)

    if df_html.equals(df_parquet):
        return

    merged = df_html.merge(df_parquet, indicator=True, how="outer")
    differences = merged[merged["_merge"] != "both"].drop(columns=["_merge"])
    raise AssertionError(f"HTML table and Parquet dataset do not match:\n{differences.to_string()}")
    merged = df_html_sorted.merge(df_parquet_sorted, indicator=True, how="outer")
    differences = merged[merged["_merge"] != "both"].drop(columns=["_merge"])
    raise AssertionError(f"HTML table and Parquet dataset do not match:\n{differences.to_string()}")
