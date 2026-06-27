from collections import Counter
import re


def generate_insights(chunks):

    if not chunks:
        return {
            "summary": "No data available",
            "keywords": [],
            "topics": [],
            "trend": "No sufficient data"
        }

    text = " ".join(chunks).lower()

    # 1. Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text)

    freq = Counter(words)
    keywords = [w for w, _ in freq.most_common(10)]

    # 2. Simple topic grouping (rule-based)
    topics = []

    if any(word in text for word in ["ai", "ml", "machine", "learning"]):
        topics.append("Artificial Intelligence")

    if any(word in text for word in ["project", "built", "developed"]):
        topics.append("Projects")

    if any(word in text for word in ["iot", "sensor", "embedded"]):
        topics.append("Embedded Systems")

    # 3. Summary
    summary = "This content mainly discusses " + ", ".join(keywords[:5])

    # 4. “Missing knowledge” hint (simple logic)
    trend = "User data shows focus on technical and project-based content"

    return {
        "summary": summary,
        "keywords": keywords,
        "topics": topics,
        "trend": trend
    }