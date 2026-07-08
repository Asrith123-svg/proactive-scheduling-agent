def assess_risk(event):
    """
    Determine if modifying this event is low-risk (safe to auto-execute)
    or high-risk (requires human confirmation).
    """
    attendees = event.get('attendees', [])

    # No attendees other than yourself = low risk, safe to auto-adjust
    if len(attendees) == 0:
        return 'low'

    # Any attendees present = high risk, changing it affects other people
    return 'high'


def describe_risk(risk_level):
    if risk_level == 'low':
        return "Low risk — no other attendees. Safe to auto-execute."
    else:
        return "High risk — other attendees involved. Requires confirmation before acting."