import math
from typing import Dict, Any, Tuple
from backend.models.schemas import BloomLevel, MasteryLevels, StudentProfile


class KnowledgeTracer:
    """
    Bayesian Knowledge Tracing (BKT) & Elo-style Cognitive Tracker.
    Models student latent mastery probability across each Bloom's taxonomy tier
    and updates scores dynamically based on quiz results and study interactions.
    """

    def __init__(
        self,
        p_guess: float = 0.20,
        p_slip: float = 0.10,
        p_transit: float = 0.15
    ):
        # BKT Parameters
        self.p_guess = p_guess      # Probability of guessing correctly without mastery
        self.p_slip = p_slip        # Probability of slipping/error despite mastery
        self.p_transit = p_transit  # Probability of learning/transitioning on each attempt

    def update_mastery(
        self,
        student: StudentProfile,
        bloom_level: BloomLevel,
        is_correct: bool,
        response_time_seconds: float = 30.0
    ) -> Tuple[MasteryLevels, Dict[str, Any]]:
        """
        Updates the student's mastery level for a specific Bloom tier using BKT.
        Applies a time-penalty/bonus based on optimal response velocity.
        """
        current_levels = student.mastery_levels
        current_score = getattr(current_levels, bloom_level.value)
        p_known = max(0.01, min(0.99, current_score / 100.0))

        # Bayesian Posterior Calculation
        if is_correct:
            numerator = p_known * (1.0 - self.p_slip)
            denominator = numerator + (1.0 - p_known) * self.p_guess
            posterior = numerator / max(1e-6, denominator)
        else:
            numerator = p_known * self.p_slip
            denominator = numerator + (1.0 - p_known) * (1.0 - self.p_guess)
            posterior = numerator / max(1e-6, denominator)

        # Transition (learning update)
        p_next = posterior + (1.0 - posterior) * self.p_transit

        # Time factor adjustment (bonus if fast & correct, small penalty if unusually slow)
        time_factor = 1.0
        if is_correct and response_time_seconds < 25.0:
            time_factor = 1.03
        elif not is_correct and response_time_seconds > 60.0:
            time_factor = 0.97

        new_score = round(min(100.0, max(0.0, p_next * 100.0 * time_factor)), 1)
        delta = round(new_score - current_score, 1)

        # Update mastery dictionary
        updated_dict = current_levels.model_dump()
        updated_dict[bloom_level.value] = new_score
        new_mastery = MasteryLevels(**updated_dict)

        # Update student in-place
        student.mastery_levels = new_mastery
        if is_correct:
            student.streak += 1
        else:
            student.streak = max(0, student.streak - 1)
        student.study_hours = round(student.study_hours + (response_time_seconds / 3600.0), 2)

        meta = {
            "bloom_level": bloom_level.value,
            "is_correct": is_correct,
            "old_score": current_score,
            "new_score": new_score,
            "score_delta": delta,
            "posterior_probability": round(posterior, 4),
            "current_streak": student.streak,
            "average_overall_mastery": new_mastery.get_average()
        }
        return new_mastery, meta

    def get_learning_diagnosis(self, student: StudentProfile) -> Dict[str, Any]:
        """
        Analyzes the student's mastery profile to diagnose strengths and learning gaps.
        """
        m = student.mastery_levels
        tiers = {
            "remembering": m.remembering,
            "understanding": m.understanding,
            "applying": m.applying,
            "analyzing": m.analyzing,
            "evaluating": m.evaluating,
            "creating": m.creating,
        }

        strongest_tier = max(tiers, key=tiers.get)
        weakest_tier = min(tiers, key=tiers.get)

        # Find bottleneck tier
        bottleneck = None
        for tier in ["remembering", "understanding", "applying", "analyzing", "evaluating", "creating"]:
            if tiers[tier] < 60.0:
                bottleneck = tier
                break

        return {
            "student_id": student.id,
            "student_name": student.name,
            "strongest_tier": {"tier": strongest_tier, "score": tiers[strongest_tier]},
            "weakest_tier": {"tier": weakest_tier, "score": tiers[weakest_tier]},
            "pedagogical_bottleneck": bottleneck or "None (Advanced mastery)",
            "average_mastery": m.get_average(),
            "readiness_for_advanced_eval": m.understanding >= 75.0 and m.applying >= 60.0
        }
