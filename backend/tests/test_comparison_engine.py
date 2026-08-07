import pandas as pd

from app.engines.comparison_engine import ComparisonEngine


def test_comparison():

    old = pd.DataFrame({

        "Age":[20,25,30],

        "Salary":[100,200,300],

    })

    new = pd.DataFrame({

        "Age":[20,25,35],

        "Salary":[120,250,320],

        "Department":[

            "IT",

            "HR",

            "IT",

        ]

    })

    engine = ComparisonEngine()

    report = engine.compare(

        old_snapshot_id=1,

        new_snapshot_id=2,

        old_df=old,

        new_df=new,

    )

    assert report.row_difference == 0
    assert report.column_difference == 1

    assert report.removed_columns == []

    assert "Age" in report.statistics_changes

    assert "Age" in report.missing_value_changes

    assert report.duplicate_changes.old.count == 0
    assert report.duplicate_changes.new.count == 0

    print('Test Done')

if __name__ == "__main__":
    test_comparison()