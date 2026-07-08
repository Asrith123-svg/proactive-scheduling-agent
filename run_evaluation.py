from decision_maker import propose_resolution
from memory import PreferenceMemory
from eval_cases import EVAL_CASES

memory = PreferenceMemory()


def resolve_with_memory(conflict_description):
    relevant = memory.retrieve_relevant(conflict_description, k=2)
    enriched = {
        'description': conflict_description,
        'relevant_preferences': relevant,
    }
    return propose_resolution(enriched), relevant


def resolve_without_memory(conflict_description):
    enriched = {
        'description': conflict_description,
        'relevant_preferences': [],  # no memory context at all
    }
    return propose_resolution(enriched), []


def score_response(response_text, expected_keywords):
    response_lower = response_text.lower()
    hits = [kw for kw in expected_keywords if kw.lower() in response_lower]
    return len(hits), hits


if __name__ == '__main__':
    total_with_memory = 0
    total_without_memory = 0

    for i, case in enumerate(EVAL_CASES):
        print(f"\n{'='*60}")
        print(f"Case {i+1}: {case['conflict_description']}")
        print('='*60)

        resp_with, retrieved = resolve_with_memory(case['conflict_description'])
        score_with, hits_with = score_response(resp_with, case['expected_keywords'])

        resp_without, _ = resolve_without_memory(case['conflict_description'])
        score_without, hits_without = score_response(resp_without, case['expected_keywords'])

        print(f"\n[WITH memory] Retrieved: {retrieved}")
        print(f"Response: {resp_with}")
        print(f"Score: {score_with}/{len(case['expected_keywords'])} keywords matched: {hits_with}")

        print(f"\n[WITHOUT memory]")
        print(f"Response: {resp_without}")
        print(f"Score: {score_without}/{len(case['expected_keywords'])} keywords matched: {hits_without}")

        total_with_memory += score_with
        total_without_memory += score_without

    print(f"\n\n{'='*60}")
    print(f"FINAL RESULTS")
    print('='*60)
    print(f"Total score WITH memory:    {total_with_memory}")
    print(f"Total score WITHOUT memory: {total_without_memory}")