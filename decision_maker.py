import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def propose_resolution(conflict):
    """Given an enriched conflict (with description + relevant_preferences), ask the LLM to propose a fix."""

    preferences_text = "\n".join(f"- {p}" for p in conflict.get('relevant_preferences', []))

    prompt = f"""You are a scheduling assistant. A calendar conflict has been detected.

Conflict:
{conflict['description']}

The user's known preferences (most relevant to this situation):
{preferences_text}

Propose 1-2 concrete resolutions for this conflict, grounded specifically in the preferences above.
Be brief and direct. Format as a numbered list. Do not explain your reasoning at length — just the proposed actions."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content