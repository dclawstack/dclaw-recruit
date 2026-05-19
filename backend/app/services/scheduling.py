"""Interview Scheduling service — calendar coordination and availability."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import UUID


@dataclass
class TimeSlot:
    start: datetime
    end: datetime
    available: bool = True


@dataclass
class SchedulingResult:
    candidate_id: UUID
    interviewer: str
    proposed_slots: list[datetime] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    timezone_note: str | None = None


def generate_available_slots(
    days_ahead: int = 14,
    business_hours_only: bool = True,
    slot_duration_minutes: int = 60,
) -> list[TimeSlot]:
    """Generate available time slots for scheduling.

    Args:
        days_ahead: How many days to look ahead
        business_hours_only: If True, only 9am-5pm slots
        slot_duration_minutes: Duration of each slot

    Returns:
        List of TimeSlot objects
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    slots = []

    for day_offset in range(1, days_ahead + 1):
        day = now + timedelta(days=day_offset)

        # Skip weekends
        if day.weekday() >= 5:
            continue

        if business_hours_only:
            start_hour = 9
            end_hour = 17
        else:
            start_hour = 0
            end_hour = 23

        current = day.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = day.replace(hour=end_hour, minute=59, second=59, microsecond=0)

        while current < end_time:
            slot_end = current + timedelta(minutes=slot_duration_minutes)
            if slot_end <= end_time:
                slots.append(TimeSlot(start=current, end=slot_end))
            current = slot_end

    return slots


def find_best_slots(
    candidate_availability: list[dict],
    interviewer_availability: list[dict],
    num_slots: int = 3,
    timezone_offset_hours: int | None = None,
) -> SchedulingResult:
    """Find overlapping available time slots between candidate and interviewer.

    Args:
        candidate_availability: List of {start, end} dicts
        interviewer_availability: List of {start, end} dicts
        num_slots: Number of best slots to return
        timezone_offset_hours: Candidate's timezone offset from UTC

    Returns:
        SchedulingResult with proposed slots and conflicts
    """
    # Simple overlap detection
    proposed = []
    conflicts = []

    all_slots = generate_available_slots(days_ahead=14)

    for slot in all_slots:
        if len(proposed) >= num_slots:
            break

        # Check candidate availability
        candidate_ok = any(
            slot.start >= datetime.fromisoformat(a["start"]).replace(tzinfo=None)
            and slot.end <= datetime.fromisoformat(a["end"]).replace(tzinfo=None)
            for a in candidate_availability
        ) if candidate_availability else True

        # Check interviewer availability
        interviewer_ok = any(
            slot.start >= datetime.fromisoformat(a["start"]).replace(tzinfo=None)
            and slot.end <= datetime.fromisoformat(a["end"]).replace(tzinfo=None)
            for a in interviewer_availability
        ) if interviewer_availability else True

        if candidate_ok and interviewer_ok:
            proposed.append(slot.start)
        elif not candidate_ok:
            conflicts.append(f"Candidate unavailable: {slot.start.isoformat()}")
        elif not interviewer_ok:
            conflicts.append(f"Interviewer unavailable: {slot.start.isoformat()}")

    tz_note = None
    if timezone_offset_hours:
        sign = "+" if timezone_offset_hours >= 0 else ""
        tz_note = f"Times are in UTC. Candidate timezone: UTC{sign}{timezone_offset_hours}"

    return SchedulingResult(
        candidate_id=UUID("00000000-0000-0000-0000-000000000000"),  # placeholder
        interviewer="TBD",
        proposed_slots=proposed,
        conflicts=conflicts[:5],
        timezone_note=tz_note,
    )


def generate_reminder_message(
    candidate_name: str,
    interviewer_name: str,
    scheduled_time: datetime,
    days_before: int = 1,
) -> str:
    """Generate a reminder message for scheduled interviews."""
    formatted_time = scheduled_time.strftime("%A, %B %d at %I:%M %p UTC")

    if days_before == 0:
        return (
            f"🔔 Reminder: Your interview is today at {formatted_time}.\n"
            f"Candidate: {candidate_name}\n"
            f"Interviewer: {interviewer_name}"
        )
    else:
        return (
            f"📅 Upcoming Interview: {candidate_name} with {interviewer_name}\n"
            f"Scheduled for {formatted_time} (in {days_before} day(s))"
        )
