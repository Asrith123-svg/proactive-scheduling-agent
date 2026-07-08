from memory import PreferenceMemory

memory = PreferenceMemory()

query = "There's a meeting scheduled at 10pm, is that a problem?"
results = memory.retrieve_relevant(query, k=2)

print("Most relevant memories:")
for r in results:
    print("-", r)
    