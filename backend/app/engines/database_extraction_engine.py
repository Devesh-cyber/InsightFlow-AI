import re

import pandas as pd
from sqlalchemy import create_engine, text

from app.models.data_source import DataSource


class DatabaseExtractionEngine:

    def extract(
        self,
        data_source: DataSource,
    ) -> pd.DataFrame:

        if data_source.source_type != "sqlite":

            raise ValueError(
                f"Unsupported source type: "
                f"{data_source.source_type}"
            )

        if not data_source.table_name:

            raise ValueError(
                "table_name is required"
            )

        if not re.match(
            r"^[A-Za-z_][A-Za-z0-9_]*$",
            data_source.table_name,
        ):

            raise ValueError(
                "Invalid table name"
            )

        engine = create_engine(
            data_source.connection_string
        )

        try:

            query = text(
                f'SELECT * FROM "{data_source.table_name}"'
            )

            with engine.connect() as connection:

                df = pd.read_sql(
                    query,
                    connection,
                )

            return df

        finally:

            engine.dispose()