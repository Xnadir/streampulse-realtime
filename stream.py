"""
Stream — generates simulated data streams and processes with AI.
"""

import os
import json
import random
import asyncio
import google.generativeai as genai
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# sample data for stream simulation
MESSAGES = [
    "Just received my order and the quality is absolutely amazing! 5 stars!",
    "The app keeps crashing every time I try to check out. Terrible experience.",
    "Pretty decent service, nothing extraordinary but gets the job done.",
    "URGENT: Server CPU usage at 98% on prod-east-2. Investigating now.",
    "This new feature update is incredible, the UI is so much smoother.",
    "Been waiting 3 weeks for a refund. Customer support is non-existent.",
    "The API response time improved by 40% after the latest optimization.",
    "Another security patch deployed. All systems nominal.",
    "Love the new dark mode! Much easier on the eyes during late night coding.",
    "WARNING: Unusual login pattern detected from IP 192.168.1.x range",
    "Product arrived damaged. Second time this month. Very disappointed.",
    "Great team meeting today. Q3 targets look very achievable.",
    "Database migration completed successfully. Zero downtime achieved!",
    "The documentation is outdated and confusing. Needs a rewrite.",
    "New user signups increased 25% week over week. Marketing push is working.",
    "CRITICAL: Payment gateway timeout errors increasing on stripe-prod",
    "Just finished the ML model training. Accuracy improved to 94.2%!",
    "This product changed my workflow completely. Can't imagine going back.",
    "Deployment failed on staging. Rolling back to previous version.",
    "Customer reported data inconsistency in the analytics dashboard.",
]

SOURCES = ["reviews", "monitoring", "social", "support", "alerts"]


async def generate_stream_item() -> dict:
    """Generate a single stream item with simulated AI analysis."""
    message = random.choice(MESSAGES)
    source = random.choice(SOURCES)

    # quick local sentiment analysis (no API call for speed)
    sentiment = _quick_sentiment(message)
    is_anomaly = _detect_anomaly(message)

    return {
        "id": datetime.now().strftime("%H%M%S%f")[:10],
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "source": source,
        "sentiment": sentiment,
        "is_anomaly": is_anomaly,
        "confidence": round(random.uniform(0.75, 0.99), 2),
    }


def _quick_sentiment(text: str) -> str:
    """Fast rule-based sentiment for streaming speed."""
    text_lower = text.lower()
    positive_words = ["amazing", "love", "great", "incredible", "improved", "successfully", "achieved", "working", "best"]
    negative_words = ["terrible", "crashing", "urgent", "warning", "critical", "damaged", "disappointed", "failed", "timeout", "errors"]

    pos = sum(1 for w in positive_words if w in text_lower)
    neg = sum(1 for w in negative_words if w in text_lower)

    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"


def _detect_anomaly(text: str) -> bool:
    """Rule-based anomaly detection for streaming."""
    anomaly_signals = ["URGENT", "CRITICAL", "WARNING", "unusual", "timeout", "failed", "crashed", "error"]
    return any(signal.lower() in text.lower() for signal in anomaly_signals)


async def analyze_batch_with_ai(messages: list[str]) -> list[dict]:
    """Use AI for batch analysis (used for deeper analysis, not streaming)."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    numbered = "\n".join(f"{i+1}. {m}" for i, m in enumerate(messages))

    prompt = f"""Analyze each message. For each, provide:
- sentiment: positive/negative/neutral
- category: review/alert/metric/update/issue
- priority: low/medium/high/critical

Return ONLY a JSON array. No explanations.

Messages:
{numbered}"""

    try:
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(temperature=0.1))
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        return json.loads(text.strip())
    except:
        return [{"sentiment": "neutral", "category": "unknown", "priority": "low"}] * len(messages)
