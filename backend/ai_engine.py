import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.database import get_database

async def fetch_live_data():
    """
    Fetch all services from the database to generate embeddings.
    """
    db = await get_database()
    services_cursor = db["services"].find({})
    services = await services_cursor.to_list(length=1000)
    return services

def prepare_text(service):
    """
    Convert service record into a single text string for vectorization.
    """
    skills_str = " ".join(service.get("skills", []))
    # Weighting certain fields by repeating them
    title = service.get('title', '')
    category = service.get('category', '')
    description = service.get('description', '')
    
    # Combined text for TF-IDF
    text = f"{title} {title} {category} {skills_str} {description}"
    return text.lower()

async def recommend_services(user_query: str, top_n: int = 5):
    """
    Main AI logic using TF-IDF (Term Frequency-Inverse Document Frequency):
    User query -> Vector Similarity -> best services
    This approach is highly robust and doesn't require complex DLLs like Torch.
    """
    # 1. Fetch live data
    services = await fetch_live_data()
    if not services:
        return []

    # 2. Prepare corpus
    service_texts = [prepare_text(s) for s in services]
    if not service_texts:
        return []

    # 3. Vectorize
    # We use char-level N-grams (3-5) to handle partial matches and typos
    vectorizer = TfidfVectorizer(
        stop_words='english',
        analyzer='char_wb', 
        ngram_range=(3, 5),
        max_features=5000
    )
    
    try:
        # Fit on services + query to ensure shared vocabulary
        all_texts = service_texts + [user_query.lower()]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Service vectors are all but the last one
        service_vectors = tfidf_matrix[:-1]
        # Query vector is the last one
        query_vector = tfidf_matrix[-1]

        # 4. Calculate Cosine Similarity
        similarity_scores = cosine_similarity(query_vector, service_vectors)[0]

        # 5. Get Top N results
        top_indices = similarity_scores.argsort()[-top_n:][::-1]

        results = []
        for idx in top_indices:
            score = float(similarity_scores[idx])
            # Lowering threshold even further for tiny datasets
            if score < 0.01: 
                continue
                
            service = services[idx]
            service["id"] = str(service["_id"])
            del service["_id"] 
            service["ai_score"] = round(score, 3)
            results.append(service)

        return results
    except Exception as e:
        print(f"❌ Recommendation Error: {e}")
        return []
