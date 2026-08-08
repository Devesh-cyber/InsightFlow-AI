from app.schemas.threshold_schema import (
    ThresholdAlert,
    ThresholdResult, ThresholdRule
)


class ThresholdEngine:

    def evaluate(
            self, report,
            rule: ThresholdRule
    ) -> ThresholdResult:

        alerts = []

        for column, comparison in (
            report.statistics_changes.items()
        ):
            old_mean = comparison.old.mean
            new_mean = comparison.new.mean

            if old_mean == 0:
                continue

            percentage_change = (
                abs(new_mean - old_mean) / abs(old_mean)
            ) * 100

            if percentage_change >= (
                rule.threshold_percentage
            ):
                direction = (
                    'up'
                    if new_mean > old_mean
                    else 'down'
                )

                alerts.append(
                    ThresholdAlert(
                        metric='mean',
                        column=column,
                        old_value=old_mean,
                        new_value=new_mean,
                        percentage_change=round(
                            percentage_change,2
                        ),
                        threshold=(
                            rule.threshold_percentage
                        ),
                        direction=direction
                    )
                )

        return ThresholdResult(
                triggered=len(alerts) > 0,
                alerts=alerts
            )