from datetime import datetime

from sqlmodel import SQLModel


class DataTypeChange(SQLModel):
    old: str
    new: str


class StatisticSummary(SQLModel):
    mean: float
    median: float
    minimum: float
    maximum: float
    std: float


class ColumnStatistics(SQLModel):
    old: StatisticSummary
    new: StatisticSummary


class MissingValueSummary(SQLModel):
    count: int
    percentage: float


class MissingValueComparison(SQLModel):
    old: MissingValueSummary
    new: MissingValueSummary
    difference: int


class DuplicateSummary(SQLModel):
    count: int
    percentage: float


class DuplicateComparison(SQLModel):
    old: DuplicateSummary
    new: DuplicateSummary
    difference: int


class DatasetComparisonReport(SQLModel):

    old_snapshot_id: int
    new_snapshot_id: int
    compared_at: datetime

    rows_before: int
    rows_after: int
    row_difference: int

    columns_before: int
    columns_after: int
    column_difference: int

    added_columns: list[str] = []
    removed_columns: list[str] = []

    datatype_changes: dict[str, DataTypeChange] = {}

    statistics_changes: dict[str, ColumnStatistics] = {}

    missing_value_changes: dict[
        str,
        MissingValueComparison,
    ] = {}

    duplicate_changes: DuplicateComparison | None = None