from datetime import datetime

import pandas as pd

from app.engines.schema_engine import SchemaEngine
from app.engines.statistics_engine import StatisticsEngine
from app.engines.missing_value_engine import MissingValueEngine
from app.engines.duplicate_engine import DuplicateEngine

from app.schemas.comparison_schema import (
    DatasetComparisonReport,
)


class ComparisonEngine:

    def __init__(self):

        self.schema_engine = SchemaEngine()

        self.statistics_engine = StatisticsEngine()

        self.missing_engine = MissingValueEngine()

        self.duplicate_engine = DuplicateEngine()

    def compare(
        self,
        old_snapshot_id: int,
        new_snapshot_id: int,
        old_df: pd.DataFrame,
        new_df: pd.DataFrame,
    ) -> DatasetComparisonReport:

        report = DatasetComparisonReport(

            old_snapshot_id=old_snapshot_id,

            new_snapshot_id=new_snapshot_id,

            compared_at=datetime.utcnow(),

            rows_before=len(old_df),

            rows_after=len(new_df),

            row_difference=len(new_df) - len(old_df),

            columns_before=len(old_df.columns),

            columns_after=len(new_df.columns),

            column_difference=(
                len(new_df.columns)
                - len(old_df.columns)
            ),

        )

        # ---------- Schema ----------
        schema_result = self.schema_engine.compare(
            old_df,
            new_df,
        )

        report.added_columns = schema_result["added_columns"]

        report.removed_columns = schema_result["removed_columns"]

        report.datatype_changes = schema_result["datatype_changes"]


        # ---------- Statistics ----------
        report.statistics_changes = (
            self.statistics_engine.compare(
                old_df,
                new_df,
            )
        )

        # ---------- Missing ----------
        report.missing_value_changes = (
            self.missing_engine.compare(
                old_df,
                new_df,
            )
        )

        # ---------- Duplicate ----------
        report.duplicate_changes = (
            self.duplicate_engine.compare(
                old_df,
                new_df,
            )
        )

        return report