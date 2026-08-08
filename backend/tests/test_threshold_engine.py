from types import SimpleNamespace

from app.engines.threshold_engine import (
    ThresholdEngine,
)

from app.schemas.threshold_schema import (
    ThresholdRule,
)


def test_threshold_triggered():

    comparison = SimpleNamespace(

        old=SimpleNamespace(
            mean=100.0
        ),

        new=SimpleNamespace(
            mean=120.0
        ),
    )

    report = SimpleNamespace(

        statistics_changes={
            "Sales": comparison
        }
    )

    engine = ThresholdEngine()

    result = engine.evaluate(
        report=report,
        rule=ThresholdRule(
            threshold_percentage=10
        ),
    )

    assert result.triggered is True

    assert len(result.alerts) == 1

    assert result.alerts[0].column == "Sales"

    assert result.alerts[0].direction == "up"

    assert result.alerts[0].percentage_change == 20


def test_threshold_not_triggered():

    comparison = SimpleNamespace(

        old=SimpleNamespace(
            mean=100.0
        ),

        new=SimpleNamespace(
            mean=105.0
        ),
    )

    report = SimpleNamespace(

        statistics_changes={
            "Sales": comparison
        }
    )

    engine = ThresholdEngine()

    result = engine.evaluate(
        report=report,
        rule=ThresholdRule(
            threshold_percentage=10
        ),
    )

    assert result.triggered is False

    assert len(result.alerts) == 0