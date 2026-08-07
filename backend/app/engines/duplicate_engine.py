import pandas as pd
from app.schemas.comparison_schema import(
    DuplicateSummary, DuplicateComparison
)


class DuplicateEngine:

    def compare(
            self, new_df: pd.DataFrame, old_df: pd.DataFrame
    ) -> DuplicateComparison:

        old_duplicates = int(
            old_df.duplicated().sum()
        )

        new_duplicates = int(
            new_df.duplicated().sum()
        )

        old_percentage = (
            old_duplicates / len(old_df) * 100
        ) if len(old_df) > 0 else 0

        new_percentage = (
            new_duplicates / len(new_df) * 100
        ) if len(new_df) > 0 else 0

        return DuplicateComparison(

            old=DuplicateSummary(
                count=old_duplicates,
                percentage=round(old_percentage, 2),
            ),

            new=DuplicateSummary(
                count=new_duplicates,
                percentage=round(new_percentage, 2),
            ),

            difference=new_duplicates - old_duplicates,
        )