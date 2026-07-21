"""
validator.py

Data Quality Validator for the N100 Financial Intelligence Platform.
"""

import pandas as pd


class DataValidator:

    def __init__(self):
        self.failures = []

    def add_failure(self, rule, severity, table, row, message):
        self.failures.append({
            "rule": rule,
            "severity": severity,
            "table": table,
            "row": row,
            "message": message
        })

    def dq01_primary_key(self, df, column, table):
        """
        DQ-01:
        Primary key must be unique.
        """

        duplicates = df[df[column].duplicated()]

        for idx in duplicates.index:
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table,
                idx,
                f"Duplicate primary key: {df.loc[idx, column]}"
            )

    def dq02_mandatory_fields(self, df, columns, table):
        """
        DQ-02:
        Mandatory fields cannot contain NULL values.
        """

        for column in columns:
            missing_rows = df[df[column].isna()].index

            for idx in missing_rows:
                self.add_failure(
                    "DQ-02",
                    "HIGH",
                    table,
                    idx,
                    f"Missing mandatory field: {column}"
                )

    def dq03_data_type(self, df, column, expected_type, table):
        """
        DQ-03:
        Validate column data types.
        """

        invalid_rows = []

        if expected_type == "numeric":

            invalid_rows = df[
                pd.to_numeric(df[column], errors="coerce").isna()
                & df[column].notna()
            ].index

        elif expected_type == "string":

            invalid_rows = df[
                ~df[column].apply(lambda x: isinstance(x, str))
                & df[column].notna()
            ].index

        elif expected_type == "date":

            invalid_rows = df[
                pd.to_datetime(df[column], errors="coerce").isna()
                & df[column].notna()
            ].index

        for idx in invalid_rows:
            self.add_failure(
                "DQ-03",
                "HIGH",
                table,
                idx,
                f"Invalid datatype in column: {column}"
            )

    def dq04_duplicate_records(self, df, table):
        """
        DQ-04:
        Detect duplicate records.
        """

        duplicates = df[df.duplicated(keep="first")]

        for idx in duplicates.index:
            self.add_failure(
                "DQ-04",
                "MEDIUM",
                table,
                idx,
                "Duplicate record found"
            )

    def dq05_non_negative_values(self, df, column, table):
        """
        DQ-05:
        Numeric values should not be negative.
        """

        invalid_rows = df[
            pd.to_numeric(df[column], errors="coerce") < 0
        ].index

        for idx in invalid_rows:
            self.add_failure(
                "DQ-05",
                "HIGH",
                table,
                idx,
                f"Negative value found in column: {column}"
            )

    def dq06_referential_integrity(
        self,
        df,
        column,
        reference_df,
        reference_column,
        table
    ):
        """
        DQ-06:
        Check whether values exist in reference table.
        """

        invalid_rows = df[
            ~df[column].isin(reference_df[reference_column])
        ].index

        for idx in invalid_rows:
            self.add_failure(
                "DQ-06",
                "HIGH",
                table,
                idx,
                f"Invalid reference value: {df.loc[idx, column]}"
            )

    def export_failures(self, output_path):
        """
        Export validation failures to CSV.
        """

        pd.DataFrame(self.failures).to_csv(
            output_path,
            index=False
        )