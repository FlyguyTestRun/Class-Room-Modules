from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
import datetime

class EmotionalState(Enum):
    CALM = "calm"
    AGITATED = "agitated"
    GRIEVING = "grieving"
    RUMINATING = "ruminating"
    HOPEFUL = "hopeful"
    RESENTFUL = "resentful"        # Added – common in betrayal entries
    ANXIOUS = "anxious"            # Added – frequent trigger

class InteractionType(Enum):
    INCOMING_TEXT = "incoming_text"
    MEMORY_RECALL = "memory_recall"
    DECISION_CHECK = "decision_check"
    BOUNDARY_TEST = "boundary_test"
    DATING_CONTEXT = "dating_context"
    EX_PARTNER_CONTACT = "ex_partner_contact"  # New – very common trigger

@dataclass
class StoicResponse:
    message: str
    tone: str
    boundary_enforced: bool
    recommended_action: Optional[str] = None
    timestamp: datetime.datetime = datetime.datetime.now()

class StoicFriendAgent:
    """
    Stoic Friend Agent – Masculine Elder Voice
    Core role: Preserve dignity. Convert emotion into clarity and action.
    """

    def __init__(self, name: str = "The Masculine Elder"):
        self.name = name
        self.core_principles = [
            "Do not explain yourself to someone who has already decided.",
            "Warmth without structure is self-betrayal.",
            "Grief is honored. Rumination is interrupted.",
            "Presence is power. Absence is leverage.",
            "Self-respect precedes reconciliation.",
            "A man's word is his bond. His silence is his boundary."
        ]

    def assess_state(self, user_input: str) -> EmotionalState:
        lowered = user_input.lower()
        
        if any(word in lowered for word in ["miss", "hope", "maybe", "if only", "reach out"]):
            return EmotionalState.HOPEFUL
        if any(word in lowered for word in ["angry", "resent", "unfair", "pissed", "furious"]):
            return EmotionalState.RESENTFUL
        if any(word in lowered for word in ["sad", "loss", "grief", "cry", "heartbroken"]):
            return EmotionalState.GRIEVING
        if any(word in lowered for word in ["replay", "thinking", "over and over", "can't stop"]):
            return EmotionalState.RUMINATING
        if any(word in lowered for word in ["anxious", "worried", "nervous", "panic"]):
            return EmotionalState.ANXIOUS

        return EmotionalState.CALM

    # Updated handlers with richer stoic flavor
    def _handle_incoming_text(self, state: EmotionalState) -> StoicResponse:
        if state in [EmotionalState.HOPEFUL, EmotionalState.RUMINATING, EmotionalState.ANXIOUS]:
            return StoicResponse(
                message=(
                    "Brother, respond once — brief, respectful, final. "
                    "Do not advance intimacy. Do not reference the past. "
                    "Your silence after that is your boundary."
                ),
                tone="contained",
                boundary_enforced=True,
                recommended_action="One reply. Then exit."
            )
        return StoicResponse(
            message="Acknowledge. Stay distant. Protect your peace.",
            tone="steady",
            boundary_enforced=True
        )

    def _handle_ex_partner_contact(self) -> StoicResponse:
        return StoicResponse(
            message=(
                "Ex-partner contact is a test of your new standards. "
                "If it costs dignity, the answer is no — without explanation."
            ),
            tone="decisive",
            boundary_enforced=True,
            recommended_action="No response, or minimal polite decline."
        )

    def _handle_boundary_test(self) -> StoicResponse:
        return StoicResponse(
            message=(
                "You do not owe emotional access without mutual respect. "
                "A real man declines without justification."
            ),
            tone="firm",
            boundary_enforced=True,
            recommended_action="Short decline. No debate."
        )

    def _handle_decision_check(self, state: EmotionalState) -> StoicResponse:
        if state == EmotionalState.GRIEVING:
            return StoicResponse(
                message=(
                    "Grief does not require contact. "
                    "Sit with the loss. Let it forge you. "
                    "No outreach until you can stand in it without crumbling."
                ),
                tone="grounded",
                boundary_enforced=True,
                recommended_action="Feel the grief. No action."
            )
        return StoicResponse(
            message="If the action costs self-respect, the price is too high.",
            tone="clear",
            boundary_enforced=True
        )

    def _handle_dating_context(self) -> StoicResponse:
        return StoicResponse(
            message=(
                "Date from abundance, not lack. "
                "Lead with curiosity, not comparison. "
                "Let her earn your investment — slowly."
            ),
            tone="steady",
            boundary_enforced=False,
            recommended_action="Meet new people. Stay grounded in your worth."
        )

    def daily_reminder(self) -> str:
        reminders = [
            "You are not late to your life. You are early to your integrity.",
            "A man's strength is measured by what he can walk away from.",
            "Peace is the highest form of victory.",
            "The man who masters himself needs no other crown."
        ]
        import random
        return random.choice(reminders)