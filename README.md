# Proactive Scheduling Agent with Hybrid Memory

An AI agent that monitors a Google Calendar in the background, detects scheduling conflicts before they become a problem, and proposes context-aware resolutions grounded in learned user preferences.

Built as an exploration of the "proactive agent + memory" pattern used in modern AI scheduling assistants — the agent acts on detected problems rather than waiting to be asked.

## How it works

1. **Calendar integration** — reads events from Google Calendar via OAuth2
2. **Conflict detection** — flags double-bookings, insufficient buffers between meetings, and meetings outside working hours (timezone-aware)
3. **Semantic memory (FAISS)** — stores user preferences as embeddings and retrieves the most relevant ones for a given conflict, using semantic similarity rather than keyword matching
4. **LLM decision layer** — combines the detected conflict with retrieved preferences and asks an LLM to propose 1-2 concrete, grounded resolutions

## Example output
\`\`\`
Conflict: There is a meeting 'Test event from agent' scheduled at 10:00 PM, outside normal working hours.

Relevant past preferences:
  - User prefers no meetings after 8pm
  - User avoids scheduling anything before 9am on Mondays

Proposed resolution:
1. Schedule the meeting on a different day at 2:00 PM.
2. Schedule the meeting at 7:00 AM on a day other than Monday, if possible.
\`\`\`

## Tech stack
Python · Google Calendar API · FAISS · Sentence Transformers · LLM API (Groq/Llama, swappable with Claude/OpenAI)

## Setup
1. Clone the repo and create a virtual environment
2. `pip install -r requirements.txt`
3. Set up Google Calendar OAuth credentials (see `calendar_auth.py`)
4. Add your LLM API key to a `.env` file: `GROQ_API_KEY=your_key_here`
5. Run `python seed_memory.py` to seed initial preferences
6. Run `python conflict_detector.py` to detect conflicts and get proposed resolutions

## What's next
- Risk-tiered autonomous execution (auto-resolve low-risk conflicts, ask confirmation on higher-stakes ones)
- Evaluation comparing retrieval-based memory vs. fine-tuned personalization for decision quality
- Simple dashboard for reviewing pending/executed actions

## Author
Kambam Asrith — [LinkedIn](https://linkedin.com/in/asrithsharma) · [GitHub](https://github.com/Asrith123-svg)