from memory import PreferenceMemory

memory = PreferenceMemory()


def describe_conflict(conflict):
    """Turn a conflict dict into a plain-English sentence for memory lookup."""
    if conflict['type'] == 'outside_working_hours':
        time_str = conflict['start'].strftime('%I:%M %p')
        return f"There is a meeting '{conflict['event']}' scheduled at {time_str}, outside normal working hours."

    elif conflict['type'] == 'overlap':
        return f"'{conflict['event_a']}' overlaps with '{conflict['event_b']}' by {conflict['overlap_minutes']:.0f} minutes."

    elif conflict['type'] == 'no_buffer':
        return f"'{conflict['event_a']}' and '{conflict['event_b']}' are back-to-back with only {conflict['gap_minutes']:.0f} minutes gap."

    else:
        return "An unspecified scheduling conflict occurred."


def enrich_conflict_with_memory(conflict, k=2):
    """Attach relevant past preferences to a conflict."""
    query_text = describe_conflict(conflict)
    relevant_memories = memory.retrieve_relevant(query_text, k=k)

    conflict['description'] = query_text
    conflict['relevant_preferences'] = relevant_memories
    return conflict