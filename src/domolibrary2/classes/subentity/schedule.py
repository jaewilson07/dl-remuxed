"""A class-based approach for interpreting Domo schedule configurations"""

__all__ = [
    "DomoSchedule_Base",
    "DomoAdvancedSchedule",
    "DomoCronSchedule",
    "DomoSimpleSchedule",
    "ScheduleFrequencyEnum",
    "ScheduleType",
]

import datetime as dt
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

# from ...client.auth import DomoAuth
from ...client.entities import DomoBase, DomoEnumMixin


class ScheduleFrequencyEnum(DomoEnumMixin, Enum):
    """Common schedule frequency types"""

    MANUAL = "MANUAL"
    ONCE = "ONCE"
    MINUTELY = "MINUTELY"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    CUSTOM_CRON = "CUSTOM_CRON"


class ScheduleType(DomoEnumMixin, Enum):
    """Schedule configuration types"""

    SIMPLE = "SIMPLE"
    ADVANCED = "ADVANCED"
    CRON = "CRON"


@dataclass
class DomoSchedule_Base(DomoBase, ABC):
    """Base class for interpreting and managing Domo schedule configurations"""

    # Raw schedule data
    schedule_start_date: Optional[dt.datetime] = None

    # Interpreted schedule information
    frequency: ScheduleFrequencyEnum = ScheduleFrequencyEnum.MANUAL
    schedule_type: ScheduleType = ScheduleType.SIMPLE

    # Detailed frequency information
    interval: int = 1
    minute: Optional[int] = None
    hour: Optional[int] = None
    day_of_week: Optional[list[int]] = None  # 0=Sunday, 6=Saturday
    day_of_month: Optional[list[int]] = None
    month: Optional[list[int]] = None

    # Schedule metadata
    timezone: Optional[str] = None
    is_active: bool = True
    next_run_time: Optional[dt.datetime] = None

    # Raw data for reference
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    parent: Any = None  # DomoDataset, DomoStream, DomoDataflow

    def __post_init__(self):
        """Post-initialization to interpret the schedule configuration"""
        self._interpret_schedule()

    @abstractmethod
    def _interpret_schedule(self):
        """Interpret the schedule configuration from raw data - implemented by subclasses"""
        pass

    @staticmethod
    def _extract_schedule_components(schedule_data: dict[str, Any]) -> dict[str, Any]:
        """Extract schedule components from advanced JSON configuration"""
        components = {
            "timezone": schedule_data.get("timezone"),
            "interval": schedule_data.get("interval", 1),
            "minute": schedule_data.get("minute"),
            "hour": schedule_data.get("hour"),
            "day_of_week": schedule_data.get("daysOfWeek"),
            "day_of_month": schedule_data.get("daysOfMonth"),
            "month": schedule_data.get("months"),
        }

        # Extended parsing for 'type' and 'at' fields
        type_map = {
            "MINUTE": ScheduleFrequencyEnum.MINUTELY,
            "HOUR": ScheduleFrequencyEnum.HOURLY,
            "DAY": ScheduleFrequencyEnum.DAILY,
            "WEEK": ScheduleFrequencyEnum.WEEKLY,
            "MONTH": ScheduleFrequencyEnum.MONTHLY,
            "YEAR": ScheduleFrequencyEnum.YEARLY,
        }
        if "type" in schedule_data:
            type_str = str(schedule_data["type"]).upper()
            components["frequency"] = type_map.get(
                type_str, ScheduleFrequencyEnum.CUSTOM_CRON
            )
        else:
            components["frequency"] = ScheduleFrequencyEnum.CUSTOM_CRON

        # Parse 'at' field for hour and minute
        at_str = schedule_data.get("at")
        if at_str:
            # Expect format like '09:02 AM' or '14:30'
            import re

            match = re.match(
                r"(\d{1,2}):(\d{2})\s*(AM|PM)?", at_str.strip(), re.IGNORECASE
            )
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))
                ampm = match.group(3)
                if ampm:
                    if ampm.upper() == "PM" and hour < 12:
                        hour += 12
                    elif ampm.upper() == "AM" and hour == 12:
                        hour = 0
                components["hour"] = hour
                components["minute"] = minute

        # Determine frequency from explicit 'frequency' field if present
        if schedule_data.get("frequency"):
            freq_str = schedule_data["frequency"].upper()
            if freq_str in [f.value for f in ScheduleFrequencyEnum]:
                components["frequency"] = ScheduleFrequencyEnum(freq_str)

        return components

    @staticmethod
    def _normalize_expression(expression: str) -> str:
        """Normalize schedule expression for parsing"""
        return expression.upper().strip() if expression else ""

    @staticmethod
    def _detect_expression_type(
        expr: str,
    ) -> tuple[ScheduleFrequencyEnum, ScheduleType]:
        """Detect the type and frequency from expression"""
        # Manual execution
        if expr in ["MANUAL", "NONE", ""]:
            return ScheduleFrequencyEnum.MANUAL, ScheduleType.SIMPLE

        # Once execution
        if expr in ["ONCE", "RUN_ONCE"]:
            return ScheduleFrequencyEnum.ONCE, ScheduleType.SIMPLE

        # Default for expressions that need further parsing
        return ScheduleFrequencyEnum.CUSTOM_CRON, ScheduleType.CRON

    def _is_cron_expression(self, expr: str) -> bool:
        """Check if expression looks like a cron expression"""
        # Basic cron has 5-6 fields separated by spaces
        parts = expr.split()
        return len(parts) >= 5 and len(parts) <= 6

    @staticmethod
    def _parse_cron_components(expr: str) -> dict[str, Any]:
        """Parse cron expression components and return parsed data"""
        parts = expr.split()

        if len(parts) < 5:
            return {"frequency": ScheduleFrequencyEnum.CUSTOM_CRON}

        minute_part, hour_part, day_month_part, month_part, day_week_part = parts[:5]

        result = {
            "frequency": ScheduleFrequencyEnum.CUSTOM_CRON,
            "minute": None,
            "hour": None,
        }

        # Extract specific numeric values
        try:
            if minute_part.isdigit():
                result["minute"] = int(minute_part)
            if hour_part.isdigit():
                result["hour"] = int(hour_part)
        except ValueError:
            pass

        # Infer frequency from pattern
        if minute_part != "*" and hour_part == "*":
            result["frequency"] = ScheduleFrequencyEnum.HOURLY
        elif minute_part != "*" and hour_part != "*" and day_month_part == "*":
            result["frequency"] = ScheduleFrequencyEnum.DAILY
        elif day_week_part != "*":
            result["frequency"] = ScheduleFrequencyEnum.WEEKLY
        elif day_month_part != "*":
            result["frequency"] = ScheduleFrequencyEnum.MONTHLY

        return result

    def _parse_cron_expression(self, expr: str):
        """Parse a cron expression (simplified)"""
        cron_data = self._parse_cron_components(expr)

        # Apply parsed data to instance
        self.frequency = cron_data["frequency"]
        if cron_data["minute"] is not None:
            self.minute = cron_data["minute"]
        if cron_data["hour"] is not None:
            self.hour = cron_data["hour"]

    @staticmethod
    def _parse_simple_expression_components(expr: str) -> dict[str, Any]:
        """Parse simple schedule expression and return components"""
        expr_lower = expr.lower()

        # Define patterns for different time units
        patterns = [
            (r"(\d+)\s*minute", ScheduleFrequencyEnum.MINUTELY),
            (r"(\d+)\s*hour", ScheduleFrequencyEnum.HOURLY),
            (r"(\d+)\s*day", ScheduleFrequencyEnum.DAILY),
            (r"(\d+)\s*week", ScheduleFrequencyEnum.WEEKLY),
            (r"(\d+)\s*month", ScheduleFrequencyEnum.MONTHLY),
        ]

        # Check for daily patterns
        if "daily" in expr_lower:
            match = re.search(r"(\d+)\s*daily", expr_lower)
            interval = int(match.group(1)) if match else 1
            return {"frequency": ScheduleFrequencyEnum.DAILY, "interval": interval}

        # Check other patterns
        for pattern, frequency in patterns:
            if frequency.value.lower()[:-2] in expr_lower:  # Remove 'LY' suffix
                match = re.search(pattern, expr_lower)
                interval = int(match.group(1)) if match else 1
                return {"frequency": frequency, "interval": interval}

        return {"frequency": ScheduleFrequencyEnum.CUSTOM_CRON, "interval": 1}

    def _parse_simple_expression(self, expr: str):
        """Parse simple schedule expressions"""
        components = self._parse_simple_expression_components(expr)

        self.frequency = components["frequency"]
        self.interval = components["interval"]

    def _infer_frequency_from_components(self):
        """Infer frequency based on available time components"""
        if self.day_of_week is not None:
            self.frequency = ScheduleFrequencyEnum.WEEKLY
        elif self.day_of_month is not None:
            self.frequency = ScheduleFrequencyEnum.MONTHLY
        elif self.month is not None:
            self.frequency = ScheduleFrequencyEnum.YEARLY
        elif self.hour is not None:
            self.frequency = ScheduleFrequencyEnum.DAILY
        elif self.minute is not None:
            self.frequency = ScheduleFrequencyEnum.HOURLY
        else:
            self.frequency = ScheduleFrequencyEnum.CUSTOM_CRON

    @staticmethod
    def _extract_field_mappings(obj: dict[str, Any]) -> dict[str, Any]:
        """Extract and map field names from input dictionary"""
        return {
            "start_date_raw": obj.get("scheduleStartDate") or obj.get("startDate"),
            "schedule_expr": obj.get("scheduleExpression") or obj.get("expression"),
            "advanced_json": obj.get("advancedScheduleJson")
            or obj.get("advancedSchedule"),
            "timezone": obj.get("timezone"),
            "is_active": obj.get("isActive", True),
        }

    @staticmethod
    def _parse_datetime_input(date_input: Any) -> Optional[dt.datetime]:
        """Parse various datetime input formats into datetime object"""
        if not date_input:
            return None

        # String formats
        if isinstance(date_input, str):
            # Try ISO format first
            try:
                return dt.datetime.fromisoformat(date_input.replace("Z", "+00:00"))
            except ValueError:
                pass

            # Try standard format
            try:
                return dt.datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                pass

            # Try other common formats
            formats_to_try = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%m/%d/%Y %H:%M:%S",
                "%m/%d/%Y",
            ]

            for fmt in formats_to_try:
                try:
                    return dt.datetime.strptime(date_input, fmt)
                except ValueError:
                    continue

        # Numeric timestamp (assuming milliseconds)
        elif isinstance(date_input, (int, float)):
            try:
                # Handle both seconds and milliseconds timestamps
                if date_input > 1e10:  # Likely milliseconds
                    return dt.datetime.fromtimestamp(date_input / 1000)
                else:  # Likely seconds
                    return dt.datetime.fromtimestamp(date_input)
            except (ValueError, OSError):
                pass

        return None

    @staticmethod
    def _parse_json_input(json_input: Any) -> Optional[dict[str, Any]]:
        """Parse JSON input that might be string or dict"""
        if not json_input:
            return None

        if isinstance(json_input, dict):
            return json_input

        if isinstance(json_input, str):
            try:
                return json.loads(json_input)
            except json.JSONDecodeError:
                return None

        return None

    def to_dict(self, override_fn: Optional[Callable] = None) -> dict[str, Any]:
        if override_fn:
            return override_fn(self)

        """Convert schedule to dictionary format"""
        result = super().to_dict()
        result.update(
            {
                "frequency": self.frequency.value,
                "scheduleType": self.schedule_type.value,
                "interval": self.interval,
                "isActive": self.is_active,
            }
        )

        if self.schedule_start_date:
            result["scheduleStartDate"] = self.schedule_start_date.isoformat()

        if self.day_of_week is not None:
            result["dayOfWeek"] = self.day_of_week

        if self.day_of_month is not None:
            result["dayOfMonth"] = self.day_of_month

        if self.next_run_time:
            result["nextRunTime"] = self.next_run_time.isoformat()

        return result

    def get_human_readable_schedule(self) -> str:
        """Get a human-readable description of the schedule"""
        if self.frequency == ScheduleFrequencyEnum.MANUAL:
            return "Manual execution"

        if self.frequency == ScheduleFrequencyEnum.ONCE:
            if self.schedule_start_date:
                return (
                    f"Run once on {self.schedule_start_date.strftime('%Y-%m-%d %H:%M')}"
                )
            return "Run once"

        base_desc = ""

        if self.frequency == ScheduleFrequencyEnum.MINUTELY:
            base_desc = f"Every {self.interval} minute(s)"
        elif self.frequency == ScheduleFrequencyEnum.HOURLY:
            base_desc = f"Every {self.interval} hour(s)"
            if self.minute is not None:
                base_desc += f" at {self.minute:02d} minutes past the hour"
        elif self.frequency == ScheduleFrequencyEnum.DAILY:
            base_desc = f"Every {self.interval} day(s)"
            if self.hour is not None and self.minute is not None:
                base_desc += f" at {self.hour:02d}:{self.minute:02d}"
        elif self.frequency == ScheduleFrequencyEnum.WEEKLY:
            base_desc = f"Every {self.interval} week(s)"
            if self.day_of_week:
                days = [
                    "Sunday",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                ]
                day_names = [days[day] for day in self.day_of_week if 0 <= day <= 6]
                base_desc += f" on {', '.join(day_names)}"
            if self.hour is not None and self.minute is not None:
                base_desc += f" at {self.hour:02d}:{self.minute:02d}"
        elif self.frequency == ScheduleFrequencyEnum.MONTHLY:
            base_desc = f"Every {self.interval} month(s)"
            if self.day_of_month:
                base_desc += f" on day(s) {', '.join(map(str, self.day_of_month))}"
            if self.hour is not None and self.minute is not None:
                base_desc += f" at {self.hour:02d}:{self.minute:02d}"
        elif self.frequency == ScheduleFrequencyEnum.YEARLY:
            base_desc = f"Every {self.interval} year(s)"
            if self.month:
                month_names = [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
                month_names_list = [
                    month_names[m - 1] for m in self.month if 1 <= m <= 12
                ]
                base_desc += f" in {', '.join(month_names_list)}"
            if self.day_of_month:
                base_desc += f" on day(s) {', '.join(map(str, self.day_of_month))}"
        elif self.frequency == ScheduleFrequencyEnum.CUSTOM_CRON:
            base_desc = "Custom schedule"

        if self.timezone:
            base_desc += f" ({self.timezone})"

        if not self.is_active:
            base_desc += " [INACTIVE]"

        return base_desc

    def is_due_now(self, current_time: Optional[dt.datetime] = None) -> bool:
        """Check if the schedule is due to run now (simplified logic)"""
        if not self.is_active or self.frequency == ScheduleFrequencyEnum.MANUAL:
            return False

        if current_time is None:
            current_time = dt.datetime.now()

        if self.schedule_start_date and current_time < self.schedule_start_date:
            return False

        # This is a simplified check - real implementation would need more complex logic
        # based on the specific schedule configuration
        return False  # Placeholder

    def __str__(self) -> str:
        return self.get_human_readable_schedule()

    def __repr__(self) -> str:
        return f"DomoSchedule(frequency={self.frequency.value}, type={self.schedule_type.value})"

    def export_as_dict(self, override_fn: Optional[Callable] = None) -> dict[str, Any]:
        """
        Export the schedule as a unified dictionary format.
        Args:
            override_fn: Optional function to override export logic.
        Returns:
            dict: Unified schedule dictionary.
        """
        if override_fn:
            return override_fn(self)

        # Unified schedule dict
        result = {
            "humanReadable": self.get_human_readable_schedule(),
            "frequency": self.frequency.value if self.frequency else None,
            "scheduleType": (self.schedule_type.value if self.schedule_type else None),
            "interval": self.interval,
            "minute": self.minute,
            "hour": self.hour,
            "dayOfWeek": self.day_of_week,
            "dayOfMonth": self.day_of_month,
            "month": self.month,
            "scheduleStartDate": (
                self.schedule_start_date.isoformat()
                if self.schedule_start_date
                else None
            ),
            "timezone": self.timezone,
            "isActive": self.is_active,
            "nextRunTime": (
                self.next_run_time.isoformat() if self.next_run_time else None
            ),
        }

        # Optionally include raw expression or advanced config if present
        if hasattr(self, "schedule_expression") and self.schedule_expression:
            result["expression"] = self.schedule_expression
        if hasattr(self, "advanced_schedule_json") and self.advanced_schedule_json:
            result["advancedScheduleJson"] = self.advanced_schedule_json

        return result


@dataclass
class DomoAdvancedSchedule(DomoSchedule_Base):
    """Schedule based on advanced JSON configuration"""

    advanced_schedule_json: Optional[dict[str, Any]] = None

    def _interpret_schedule(self):
        """Interpret advanced schedule JSON configuration"""
        if not self.advanced_schedule_json:
            return

        self.schedule_type = ScheduleType.ADVANCED

        # Extract components using utility function
        components = self._extract_schedule_components(self.advanced_schedule_json)

        # Apply components to instance
        self.timezone = components["timezone"]
        self.interval = components["interval"]
        self.minute = components["minute"]
        self.hour = components["hour"]
        self.day_of_week = components["day_of_week"]
        self.day_of_month = components["day_of_month"]
        self.month = components["month"]
        self.frequency = components["frequency"]

        # Determine frequency based on available components if not explicitly set
        if components[
            "frequency"
        ] == ScheduleFrequencyEnum.CUSTOM_CRON and not self.advanced_schedule_json.get(
            "frequency"
        ):
            self._infer_frequency_from_components()

    @classmethod
    def from_dict(
        cls,
        obj: dict[str, Any],
        # auth: Optional[DomoAuth] = None,
        parent: Any | None = None,
        **kwargs,
    ) -> "DomoAdvancedSchedule":
        """Create DomoAdvancedSchedule from dictionary/API response"""
        field_mappings = cls._extract_field_mappings(obj)
        start_date = cls._parse_datetime_input(field_mappings["start_date_raw"])
        advanced_json = cls._parse_json_input(field_mappings["advanced_json"])

        return cls(
            parent=parent,
            schedule_start_date=start_date,
            advanced_schedule_json=advanced_json,
            timezone=field_mappings["timezone"],
            is_active=field_mappings["is_active"],
            raw=obj,
            **kwargs,
        )


@dataclass
class DomoCronSchedule(DomoSchedule_Base):
    """Schedule based on cron-like expressions"""

    schedule_expression: Optional[str] = None

    def _interpret_schedule(self):
        """Interpret cron-like schedule expression"""
        if not self.schedule_expression:
            return

        expr = self._normalize_expression(self.schedule_expression)

        # Detect basic expression type
        frequency, schedule_type = self._detect_expression_type(expr)
        self.frequency = frequency
        self.schedule_type = schedule_type

        # If it's a simple type, we're done
        if schedule_type == ScheduleType.SIMPLE:
            return

        # Try to parse cron expression (basic patterns)
        if self._is_cron_expression(expr):
            self._parse_cron_expression(expr)
        else:
            # Try simple frequency patterns
            self._parse_simple_expression(expr)

    @classmethod
    def from_dict(
        cls,
        obj: dict[str, Any],
        # auth: Optional[DomoAuth] = None,
        parent: Any | None = None,
        **kwargs,
    ) -> "DomoCronSchedule":
        """Create DomoCronSchedule from dictionary/API response"""
        field_mappings = cls._extract_field_mappings(obj)
        start_date = cls._parse_datetime_input(field_mappings["start_date_raw"])

        return cls(
            parent=parent,
            schedule_start_date=start_date,
            schedule_expression=field_mappings["schedule_expr"],
            timezone=field_mappings["timezone"],
            is_active=field_mappings["is_active"],
            raw=obj,
            **kwargs,
        )


@dataclass
class DomoSimpleSchedule(DomoSchedule_Base):
    """Simple schedule for manual/once execution"""

    schedule_expression: Optional[str] = None

    def _interpret_schedule(self):
        """Interpret simple schedule configuration"""
        self.schedule_type = ScheduleType.SIMPLE

        if self.schedule_expression:
            expr = self._normalize_expression(self.schedule_expression)
            frequency, _ = self._detect_expression_type(expr)
            self.frequency = frequency
        else:
            self.frequency = ScheduleFrequencyEnum.MANUAL

    @classmethod
    def from_dict(
        cls, obj: dict[str, Any], parent: Any = None, **kwargs
    ) -> "DomoSimpleSchedule":
        """Create DomoSimpleSchedule from dictionary/API response"""
        field_mappings = cls._extract_field_mappings(obj)
        start_date = cls._parse_datetime_input(field_mappings["start_date_raw"])

        return cls(
            parent=parent,
            schedule_start_date=start_date,
            schedule_expression=field_mappings["schedule_expr"],
            timezone=field_mappings["timezone"],
            is_active=field_mappings["is_active"],
            raw=obj,
            **kwargs,
        )


class DomoSchedule(DomoSchedule_Base):
    """Alias for DomoSchedule_Base to maintain backward compatibility"""

    @classmethod
    def determine_schedule_type(cls, obj: dict[str, Any]) -> type["DomoSchedule_Base"]:
        """Determine the appropriate schedule subclass based on input data"""
        field_mappings = cls._extract_field_mappings(obj)

        # Check for advanced schedule JSON
        if field_mappings["advanced_json"]:
            return DomoAdvancedSchedule

        # Check for schedule expression (cron-like)
        if field_mappings["schedule_expr"]:
            expr = cls._normalize_expression(field_mappings["schedule_expr"])
            frequency, schedule_type = cls._detect_expression_type(expr)

            if schedule_type == ScheduleType.SIMPLE:
                return DomoSimpleSchedule
            else:
                return DomoCronSchedule

        # Default to simple schedule
        return DomoSimpleSchedule

    @classmethod
    def from_parent(
        cls, parent: Any, obj: dict | None = None, **kwargs
    ) -> "DomoSchedule_Base":
        """Create schedule instance from parent entity"""

        # If called on the base class, determine the correct subclass
        schedule_class = cls.determine_schedule_type(obj)
        return schedule_class.from_dict(obj, parent=parent, **kwargs)
