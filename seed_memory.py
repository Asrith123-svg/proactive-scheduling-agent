from memory import PreferenceMemory

memory = PreferenceMemory()

memory.add_preference("User prefers no meetings after 8pm")
memory.add_preference("User likes at least 15 minutes buffer between back-to-back meetings")
memory.add_preference("User prefers afternoon slots for external client calls")
memory.add_preference("User avoids scheduling anything before 9am on Mondays")