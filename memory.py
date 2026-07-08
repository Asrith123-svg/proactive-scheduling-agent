from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

MEMORY_FILE = 'memory_store.pkl'
INDEX_FILE = 'memory_index.faiss'

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, local embedding model


class PreferenceMemory:
    def __init__(self):
        self.texts = []  # keeps the original text alongside the vectors
        self.index = None
        self._load()

    def _load(self):
        if os.path.exists(MEMORY_FILE) and os.path.exists(INDEX_FILE):
            with open(MEMORY_FILE, 'rb') as f:
                self.texts = pickle.load(f)
            self.index = faiss.read_index(INDEX_FILE)
        else:
            self.index = faiss.IndexFlatL2(384)  # 384 = embedding size for this model

    def _save(self):
        with open(MEMORY_FILE, 'wb') as f:
            pickle.dump(self.texts, f)
        faiss.write_index(self.index, INDEX_FILE)

    def add_preference(self, text, similarity_threshold=0.05):
        if len(self.texts) > 0:
            existing = self.retrieve_relevant(text, k=1)
            if existing and existing[0].strip().lower() == text.strip().lower():
                print(f"Skipped duplicate: \"{text}\"")
                return

        vector = model.encode([text])
        self.index.add(np.array(vector, dtype='float32'))
        self.texts.append(text)
        self._save()
        print(f"Stored preference: \"{text}\"")

    def retrieve_relevant(self, query, k=3):
        if len(self.texts) == 0:
            return []
        vector = model.encode([query])
        distances, indices = self.index.search(np.array(vector, dtype='float32'), k)
        results = [self.texts[i] for i in indices[0] if i < len(self.texts)]
        return results