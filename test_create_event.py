from calendar_auth import get_calendar_service

service = get_calendar_service()

event = {
    'summary': 'Test event WITH attendee',
    'start': {'dateTime': '2026-07-12T22:00:00', 'timeZone': 'Asia/Kolkata'},
    'end': {'dateTime': '2026-07-12T22:30:00', 'timeZone': 'Asia/Kolkata'},
    'attendees': [{'email': 'someone@example.com'}],
}
created_event = service.events().insert(calendarId='primary', body=event).execute()
print(f"Event created: {created_event.get('htmlLink')}")