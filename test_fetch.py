from calendar_auth import get_calendar_service
from datetime import datetime, timezone

service = get_calendar_service()

now = datetime.now(timezone.utc).isoformat()
events_result = service.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
else:
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} - {event['summary']}")