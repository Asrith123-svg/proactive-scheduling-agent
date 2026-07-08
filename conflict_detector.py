from calendar_auth import get_calendar_service
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateparser
import pytz
from conflict_memory import enrich_conflict_with_memory
from decision_maker import propose_resolution
from risk_assessor import assess_risk, describe_risk
from pending_actions import add_pending_action

LOCAL_TZ = pytz.timezone('Asia/Kolkata')


def fetch_upcoming_events(days_ahead=7):
    service = get_calendar_service()

    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=days_ahead)).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])


def get_event_times(event):
    start_raw = event['start'].get('dateTime', event['start'].get('date'))
    end_raw = event['end'].get('dateTime', event['end'].get('date'))
    start = dateparser.isoparse(start_raw).astimezone(LOCAL_TZ)
    end = dateparser.isoparse(end_raw).astimezone(LOCAL_TZ)
    return start, end


def detect_conflicts(events, buffer_minutes=10, work_start_hour=9, work_end_hour=18):
    conflicts = []
    parsed_events = []

    for event in events:
        start, end = get_event_times(event)
        parsed_events.append({
            'summary': event.get('summary', '(no title)'),
            'start': start,
            'end': end,
            'raw_event': event,
        })

    for e in parsed_events:
        if e['start'].hour < work_start_hour or e['end'].hour > work_end_hour:
            conflicts.append({
                'type': 'outside_working_hours',
                'event': e['summary'],
                'start': e['start'],
                'end': e['end'],
                'raw_events': [e['raw_event']],
            })

    for i in range(len(parsed_events) - 1):
        current = parsed_events[i]
        nxt = parsed_events[i + 1]

        gap = (nxt['start'] - current['end']).total_seconds() / 60

        if gap < 0:
            conflicts.append({
                'type': 'overlap',
                'event_a': current['summary'],
                'event_b': nxt['summary'],
                'overlap_minutes': abs(gap),
                'raw_events': [current['raw_event'], nxt['raw_event']],
            })
        elif gap < buffer_minutes:
            conflicts.append({
                'type': 'no_buffer',
                'event_a': current['summary'],
                'event_b': nxt['summary'],
                'gap_minutes': gap,
                'raw_events': [current['raw_event'], nxt['raw_event']],
            })

    return conflicts


def get_conflict_risk(conflict):
    """Check all events involved in this conflict; if any has attendees, it's high risk."""
    risks = [assess_risk(e) for e in conflict.get('raw_events', [])]
    return 'high' if 'high' in risks else 'low'


if __name__ == '__main__':
    events = fetch_upcoming_events(days_ahead=7)
    conflicts = detect_conflicts(events)

    if not conflicts:
        print("No conflicts found in the next 7 days.")
    else:
        print(f"Found {len(conflicts)} conflict(s):\n")
        for c in conflicts:
            enriched = enrich_conflict_with_memory(c)
            print(f"Conflict: {enriched['description']}")
            print("Relevant past preferences:")
            for pref in enriched['relevant_preferences']:
                print(f"  - {pref}")

            print("\nProposed resolution:")
            resolution = propose_resolution(enriched)
            print(resolution)

            risk = get_conflict_risk(enriched)
            print(f"\nRisk assessment: {describe_risk(risk)}")

            if risk == 'low':
                print("[AUTO-EXECUTE] No other attendees — this would be applied automatically.")
                print("(Note: actual calendar modification not yet implemented — this logs the decision only.)")
            else:
                add_pending_action(enriched['description'], resolution)

            print("\n" + "-"*50 + "\n")