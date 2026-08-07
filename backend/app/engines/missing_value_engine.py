import pandas as pd
from app.schemas.comparison_schema import(
    MissingValueComparison, MissingValueSummary
)


class MissingValueEngine:

    def compare(
            self,
            old_df: pd.DataFrame,
            new_df: pd.DataFrame
    ):

        result = {}

        common_columns = sorted(
            set(old_df.columns) &
            set(new_df.columns)
        )

        old_rows = len(old_df)
        new_rows = len(new_df)

        for column in common_columns:
            old_missing = int(
                old_df[column].isna().sum().sum()
            )

            new_missing = int(
                new_df[column].isna().sum().sum()
            )

            old_percentage = (
                old_missing / old_rows * 100
            ) if new_rows else 0

            new_percentage = (
                new_missing / new_rows * 100
            ) if new_rows else 0

            result[column] = MissingValueComparison(
                old = MissingValueSummary(
                    count=old_missing,

                    percentage=round(
                        old_percentage, 2
                    ),
                ),
                new=MissingValueSummary(
                    count=new_missing,
                    percentage=round(
                        new_percentage,2
                    ),
                ),
                difference=new_missing - old_missing
            )

        return result