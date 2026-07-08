from calendar_auth import get_calendar_service

service = get_calendar_service()

event = {
    'summary': 'Test event from agent',
    'start': {'dateTime': '2026-07-11T22:00:00', 'timeZone': 'Asia/Kolkata'},
'end': {'dateTime': '2026-07-11T22:30:00', 'timeZone': 'Asia/Kolkata'},
}

created_event = service.events().insert(calendarId='primary', body=event).execute()
print(f"Event created: {created_event.get('htmlLink')}")