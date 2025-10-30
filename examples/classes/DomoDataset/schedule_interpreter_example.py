import datetime
import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DomoSchedule:
    schedule_start_date: Optional[datetime.datetime] = None
    schedule_expression: Optional[str] = None
    advanced_schedule_json: Optional[Any] = None
    frequency: Optional[str] = None
    details: Optional[dict] = field(default_factory=dict)

    @classmethod
    def from_raw(
        cls,
        schedule_start_date: Optional[str],
        schedule_expression: Optional[str],
        advanced_schedule_json: Optional[str],
    ):
        # Parse start date
        start_date = None
        if schedule_start_date:
            try:
                start_date = datetime.datetime.fromisoformat(schedule_start_date)
            except Exception:
                start_date = schedule_start_date  # fallback to raw
        # Parse advanced schedule
        adv_json = None
        if advanced_schedule_json:
            try:
                adv_json = json.loads(advanced_schedule_json)
            except Exception:
                adv_json = advanced_schedule_json
        # Determine frequency
        frequency = None
        details = {}
        if schedule_expression:
            if schedule_expression.startswith("cron("):
                frequency = "cron"
                details["expression"] = schedule_expression
            elif schedule_expression.lower() in [
                "hourly",
                "daily",
                "weekly",
                "monthly",
            ]:
                frequency = schedule_expression.lower()
            else:
                frequency = "custom"
                details["expression"] = schedule_expression
        elif adv_json:
            frequency = (
                adv_json.get("type", "advanced")
                if isinstance(adv_json, dict)
                else "advanced"
            )
            details["advanced"] = adv_json
        return cls(
            schedule_start_date=start_date,
            schedule_expression=schedule_expression,
            advanced_schedule_json=adv_json,
            frequency=frequency,
            details=details,
        )

    def describe(self):
        return {
            "start_date": self.schedule_start_date,
            "frequency": self.frequency,
            "details": self.details,
        }


# Example usage
if __name__ == "__main__":
    # Sample raw schedule data
    raw_start_date = "2025-10-29T08:00:00"
    raw_expression = "cron(0 8 * * ? *)"
    raw_advanced_json = (
        '{"type": "advanced", "days": ["Monday", "Wednesday"], "time": "08:00"}'
    )

    schedule = DomoSchedule.from_raw(raw_start_date, raw_expression, raw_advanced_json)
    print(schedule)
    print(schedule.describe())
