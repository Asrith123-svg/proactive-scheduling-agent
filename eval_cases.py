EVAL_CASES = [
    {
        "conflict_description": "There is a meeting 'Client sync' scheduled at 9:30 PM, outside normal working hours.",
        "expected_keywords": ["before 8", "8pm", "earlier", "reschedule"],
    },
    {
        "conflict_description": "'Team standup' and 'Design review' are back-to-back with only 3 minutes gap.",
        "expected_keywords": ["buffer", "15 minutes", "gap", "space out"],
    },
    {
        "conflict_description": "There is a meeting 'Quick call' scheduled at 7:00 AM on Monday.",
        "expected_keywords": ["Monday", "avoid", "different day", "later"],
    },
    {
        "conflict_description": "'External vendor call' overlaps with 'Internal review' by 20 minutes.",
        "expected_keywords": ["overlap", "reschedule", "conflict"],
    },
]