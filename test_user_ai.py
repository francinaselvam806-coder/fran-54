"""
test_user_ai.py
Transformer-based Live Recommendation AI (User provided logic)
"""
import os
# Try the fix before importing torch/sentence-transformers
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    from pymongo import MongoClient
    import numpy as np
    import sys
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    sys.exit()

# DATABASE CONFIG
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "hyperlocal_gig_finder" # Using actual project DB
COLLECTION_NAME = "services"     # Using actual services collection

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("✅ MongoDB connected")
except Exception as e:
    print("❌ MongoDB connection failed")
    print(e)
    sys.exit()

print("🔄 Loading Transformer Model...")
try:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("✅ Transformer Model Loaded")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    sys.exit()

def recommend_service(user_query, top_n=5):
    records = list(collection.find({}, {"_id": 0}))
    if len(records) == 0:
        return []

    texts = []
    for r in records:
        text = f"{r.get('title','')} {r.get('category','')} {r.get('description','')} {' '.join(r.get('skills', []))}"
        texts.append(text)
    
    data_embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    user_embedding = model.encode([user_query], convert_to_numpy=True, normalize_embeddings=True)

    similarity_scores = cosine_similarity(user_embedding, data_embeddings)[0]
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "title": records[idx].get("title"),
            "score": round(float(similarity_scores[idx]), 3)
        })
    return results

if __name__ == "__main__":
    query = "I need a math tutor"
    print(f"🔍 Testing Query: '{query}'")
    results = recommend_service(query)
    if results:
        print("\n🎯 Recommendations:")
        for r in results:
            print(f"- {r['title']} (Score: {r['score']})")
    else:
        print("Empty results.")
