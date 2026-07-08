from memory import PreferenceMemory

memory = PreferenceMemory()
print(f"Total stored preferences: {len(memory.texts)}")
for i, t in enumerate(memory.texts):
    print(f"{i}: {t}")