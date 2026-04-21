import pandas as pd

class ParquetReader:
    def process(self, file_path: str, include_subfolders: bool = False) -> pd.DataFrame:
        return pd.read_parquet(file_path)