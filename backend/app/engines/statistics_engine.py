import pandas as pd
from app.schemas.comparison_schema import (
    StatisticSummary, ColumnStatistics
)

class StatisticsEngine:

    def compare(
            self, 
            old_df: pd.DataFrame,
            new_df: pd.DataFrame
    ):

        statistics = {}

        old_numeric = set(
        old_df.select_dtypes(include="number").columns
    )

        new_numeric = set(
            new_df.select_dtypes(include="number").columns
        )

        numeric_columns = sorted(
            old_numeric & new_numeric
        )

        for column in numeric_columns:
            old_summary = StatisticSummary(
                mean=float(old_df[column].mean()),
                median=float(old_df[column].median()),
                minimum=float(old_df[column].min()),
                maximum=float(old_df[column].max()),
                std=float(old_df[column].std())
            )

            new_summary = StatisticSummary(
                        mean=float(new_df[column].mean()),
                        median=float(new_df[column].median()),
                        minimum=float(new_df[column].min()),
                        maximum=float(new_df[column].max()),
                        std=float(new_df[column].std())
            )

            statistics[column] = (
                ColumnStatistics(
                    old=old_summary,
                    new=new_summary
                )
            )
        return statistics