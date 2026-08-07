from app.schemas.comparison_schema import (
    DataTypeChange
)

class SchemaEngine:

    def compare(self, old_df, new_df):

        old_columns = set(old_df.columns)
        new_columns = set(new_df.columns)
        added_columns = sorted(
            list(
                new_columns - old_columns
            )
        )
        removed_columns = sorted(
            list(
                old_columns - new_columns
            )
        )
        datatype_changes = {}
        common_columns = (
            old_columns & new_columns
        )

        for column in common_columns:
            old_type = str(
                old_df[column].dtype
            )
            new_type = str(
                new_df[column].dtype
            )
            if old_type != new_type:
                datatype_changes[column] = (
                    DataTypeChange(
                        old=old_type,
                        new=new_type
                    )
                )

        return {
            'added_columns': added_columns,
            'removed_columns': removed_columns,
            'datatype_changes': datatype_changes
        }