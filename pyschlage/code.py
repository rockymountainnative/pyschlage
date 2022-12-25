"""Objects and routines related to Schlage WiFI access codes."""

from __future__ import annotations

from dataclasses import astuple, dataclass, field
from datetime import datetime, timezone

from .common import Mutable
from .exceptions import NotAuthenticatedError

_MIN_TIME = 0
_MAX_TIME = 0xFFFFFFFF
_MIN_HOUR = 0
_MIN_MINUTE = 0
_MAX_HOUR = 23
_MAX_MINUTE = 59
_ALL_DAYS = "7F"


@dataclass
class TemporarySchedule:
    """A temporary schedule for when an AccessCode is enabled."""

    start: datetime
    end: datetime

    @classmethod
    def from_json(cls, json) -> TemporarySchedule:
        """Creates a TemporarySchedule from a JSON dict."""
        return TemporarySchedule(
            start=datetime.utcfromtimestamp(json["activationSecs"]),
            end=datetime.utcfromtimestamp(json["expirationSecs"]),
        )

    def to_json(self) -> dict:
        """Returns a JSON dict of this TemporarySchedule."""
        return {
            "activationSecs": int(self.start.replace(tzinfo=timezone.utc).timestamp()),
            "expirationSecs": int(self.end.replace(tzinfo=timezone.utc).timestamp()),
        }


@dataclass
class DaysOfWeek:
    """Enabled status for each day of the week."""

    sun: bool = True
    mon: bool = True
    tue: bool = True
    wed: bool = True
    thu: bool = True
    fri: bool = True
    sat: bool = True

    @classmethod
    def from_str(cls, s) -> DaysOfWeek:
        """Creates a DaysOfWeek from a hex string."""
        n = int(s, 16)
        return cls(*[(n & (1 << i)) != 0 for i in reversed(range(7))])

    def to_str(self) -> str:
        """Returns the string representation."""
        n = 0
        for d in astuple(self):
            n = (n << 1) | d
        return hex(n).lstrip("0x").upper()


@dataclass
class RecurringSchedule:
    """A recurring schedule for when an AccessCode is enabled."""

    days_of_week: DaysOfWeek = field(default_factory=DaysOfWeek)
    start_hour: int = _MIN_HOUR
    start_minute: int = _MIN_MINUTE
    end_hour: int = _MAX_HOUR
    end_minute: int = _MAX_MINUTE

    @classmethod
    def from_json(cls, json) -> RecurringSchedule | None:
        """Creates a RecurringSchedule from a JSON dict."""
        if not json:
            return None
        if (
            json["daysOfWeek"] == _ALL_DAYS
            and json["startHour"] == _MIN_HOUR
            and json["startMinute"] == _MIN_MINUTE
            and json["endHour"] == _MAX_HOUR
            and json["endMinute"] == _MAX_MINUTE
        ):
            return None
        return cls(
            DaysOfWeek.from_str(json["daysOfWeek"]),
            json["startHour"],
            json["startMinute"],
            json["endHour"],
            json["endMinute"],
        )

    def to_json(self) -> dict:
        """Returns a JSON dict of this RecurringSchedule."""
        return {
            "daysOfWeek": self.days_of_week.to_str(),
            "startHour": self.start_hour,
            "startMinute": self.start_minute,
            "endHour": self.end_hour,
            "endMinute": self.end_minute,
        }


@dataclass
class AccessCode(Mutable):
    """An access code for a lock."""

    name: str = ""
    code: str = ""
    schedule: TemporarySchedule | RecurringSchedule | None = None
    notify_on_use: bool = False
    disabled: bool = False
    device_id: str | None = field(default=None, repr=False)
    access_code_id: str | None = field(default=None, repr=False)

    @staticmethod
    def request_path(device_id: str, access_code_id: str | None = None) -> str:
        """Returns the request path for an AccessCode."""
        path = f"devices/{device_id}/storage/accesscode"
        if access_code_id:
            return f"{path}/{access_code_id}"
        return path

    @classmethod
    def from_json(cls, auth, json, device_id) -> AccessCode:
        """Creates an AccessCode from a JSON dict."""
        schedule = None
        if json["activationSecs"] == _MIN_TIME and json["expirationSecs"] == _MAX_TIME:
            schedule = RecurringSchedule.from_json(json["schedule1"])
        else:
            schedule = TemporarySchedule.from_json(json)

        return AccessCode(
            _auth=auth,
            device_id=device_id,
            access_code_id=json["accesscodeId"],
            name=json["friendlyName"],
            # TODO: We assume codes are always 4 characters.
            code=f"{json['accessCode']:04}",
            notify_on_use=bool(json["notification"]),
            disabled=bool(json.get("disabled", None)),
            schedule=schedule,
        )

    def to_json(self) -> dict:
        """Returns a JSON dict with this AccessCode's mutable properties."""
        json = {
            "friendlyName": self.name,
            "accessCode": int(self.code),
            "notification": int(self.notify_on_use),
            "disabled": int(self.disabled),
            "activationSecs": _MIN_TIME,
            "expirationSecs": _MAX_TIME,
            "schedule1": RecurringSchedule().to_json(),
        }
        if isinstance(self.schedule, RecurringSchedule):
            json["schedule1"] = self.schedule.to_json()
        elif self.schedule is not None:
            json.update(self.schedule.to_json())

        return json

    def refresh(self):
        """Refreshes the AccessCode state."""
        if self._auth is None:
            raise NotAuthenticatedError
        path = self.request_path(self.device_id, self.access_code_id)
        resp = self._auth.request("get", path)
        self._update_with(resp.json(), self.device_id)

    def save(self):
        """Commits changes to the access code."""
        if self._auth is None:
            raise NotAuthenticatedError
        path = self.request_path(self.device_id, self.access_code_id)
        resp = self._auth.request("put", path, json=self.to_json())
        self._update_with(resp.json(), self.device_id)

    def delete(self):
        """Deletes the access code."""
        if self._auth is None:
            raise NotAuthenticatedError
        path = self.request_path(self.device_id, self.access_code_id)
        self._auth.request("delete", path)
        self._auth = None
        self.access_code_id = None
        self.device_id = None
        self.disabled = True
