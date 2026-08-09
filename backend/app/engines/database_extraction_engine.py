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

        if not data_source.table_name and not data_source.query:

            raise ValueError(
                "Either table_name or query "
                "must be configured"
            )

        engine = create_engine(
            data_source.connection_string
        )

        try:

            if data_source.query:

                query = text(
                    data_source.query
                )

            else:

                if not re.match(
                    r"^[A-Za-z_][A-Za-z0-9_]*$",
                    data_source.table_name,
                ):

                    raise ValueError(
                        "Invalid table name"
                    )

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