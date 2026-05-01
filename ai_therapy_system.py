"""Simple AI Therapy Support System.

This module provides a lightweight, rule-based conversational support
assistant with basic sentiment detection, reflection prompts, and crisis
escalation guidance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

CRISIS_KEYWORDS = {
    "suicide",
    "kill myself",
    "end my life",
    "self harm",
    "self-harm",
    "hurt myself",
    "can't go on",
}

EMOTION_KEYWORDS = {
    "anxious": ["anxious", "anxiety", "nervous", "panic", "worried"],
    "sad": ["sad", "depressed", "down", "hopeless", "empty"],
    "angry": ["angry", "mad", "frustrated", "annoyed", "irritated"],
    "stressed": ["stressed", "overwhelmed", "burned out", "pressure"],
}


@dataclass
class SessionState:
    """Tracks user session context."""

    user_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    turn_count: int = 0
    detected_emotions: List[str] = field(default_factory=list)


class AITherapySystem:
    """A small supportive chatbot for emotional check-ins.

    This is not a medical device and does not replace licensed mental health care.
    """

    def __init__(self, user_name: str = "friend") -> None:
        self.state = SessionState(user_name=user_name)

    def analyze_message(self, message: str) -> dict:
        """Detect simple emotional cues and crisis indicators."""
        text = message.lower()
        crisis = any(keyword in text for keyword in CRISIS_KEYWORDS)
        emotions = [
            emotion
            for emotion, keywords in EMOTION_KEYWORDS.items()
            if any(keyword in text for keyword in keywords)
        ]
        return {"crisis": crisis, "emotions": emotions}

    def respond(self, message: str) -> str:
        """Generate a supportive response based on user message."""
        self.state.turn_count += 1
        analysis = self.analyze_message(message)

        if analysis["crisis"]:
            return (
                "I'm really glad you shared this. You deserve immediate support. "
                "If you might act on these thoughts, call or text 988 now (US & Canada), "
                "or your local emergency number. If you want, we can also make a tiny "
                "step-by-step safety plan together right now."
            )

        if analysis["emotions"]:
            for emotion in analysis["emotions"]:
                if emotion not in self.state.detected_emotions:
                    self.state.detected_emotions.append(emotion)

            primary = analysis["emotions"][0]
            prompts = {
                "anxious": "Would a 60-second breathing reset help right now?",
                "sad": "Do you want to talk about what feels heaviest today?",
                "angry": "Would it help to unpack what triggered that feeling?",
                "stressed": "Would you like to prioritize just one manageable next step?",
            }
            return (
                f"It sounds like you're feeling {primary}. "
                "Thanks for being open about it. "
                f"{prompts[primary]}"
            )

        return (
            "Thank you for sharing that. I'm here with you. "
            "What has your day felt like emotionally—calm, stressed, sad, or something else?"
        )


def run_cli() -> None:
    """Run an interactive command-line chat session."""
    print("AI Therapy Support System")
    print("Note: This is supportive coaching, not professional mental health treatment.")
    name = input("What's your name? ").strip() or "friend"

    bot = AITherapySystem(user_name=name)
    print(f"Hi {name}. You can type 'exit' to stop. How are you feeling today?")

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in {"exit", "quit"}:
            print("Bot: Thanks for talking today. Please take gentle care of yourself.")
            break
        print(f"Bot: {bot.respond(user_message)}")


if __name__ == "__main__":
    run_cli()
