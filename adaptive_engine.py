"""
Advanced Adaptive Engine with Decaying Performance Score (P-Score)
Handles difficulty transitions based on fluency, accuracy, and decay mechanics.
"""

class AdaptiveEngine:
    """
    Manages difficulty using a Decaying Performance Score system.
    
    The P-Score system provides superior handling of noisy/inconsistent performance
    compared to simple rule-based systems by:
    - Rewarding both accuracy and fluency (time-based)
    - Applying strong penalties for incorrect answers
    - Using decay to prevent stagnation and require continuous positive performance
    """
    
    def __init__(self):
        self.p_score = 0.0
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.current_difficulty_index = 0  # Start at Easy
        self.decay_factor = 0.9
        
    @property
    def current_difficulty(self):
        """Get current difficulty level as string."""
        return self.difficulty_levels[self.current_difficulty_index]
    
    def update_performance(self, is_correct: bool, response_time: float) -> dict:
        """
        Update P-Score based on performance and return transition info.
        
        P-Score Update Rules:
        - High Fluency (Correct & Time ≤ 5s): +2 points
        - Accuracy (Correct & Time > 5s): +1 point  
        - Inaccurate (Incorrect): -3 points
        - Decay: P-Score × 0.9 after every turn
        
        Args:
            is_correct: Whether the answer was correct
            response_time: Time taken to answer in seconds
            
        Returns:
            dict: Contains score changes, transitions, and rationale
        """
        old_score = self.p_score
        old_difficulty = self.current_difficulty
        
        # Apply performance-based score update
        if is_correct:
            if response_time <= 5.0:
                # High Fluency: Clear mastery demonstrated
                self.p_score += 2
                rationale = "High Fluency - Correct answer with quick response"
            else:
                # Accuracy: Mastery but lacks fluency
                self.p_score += 1
                rationale = "Accuracy - Correct but slow response"
        else:
            # Strong penalty for knowledge gaps
            self.p_score -= 3
            rationale = "Inaccurate - Incorrect answer indicates knowledge gap"
        
        # Apply decay factor to mitigate inconsistent performance
        self.p_score *= self.decay_factor
        
        # Check for difficulty transitions
        transition_occurred = self._check_difficulty_transition()
        
        return {
            'old_score': old_score,
            'new_score': self.p_score,
            'score_change': self.p_score - old_score * self.decay_factor,
            'old_difficulty': old_difficulty,
            'new_difficulty': self.current_difficulty,
            'transition_occurred': transition_occurred,
            'rationale': rationale
        }
    
    def _check_difficulty_transition(self) -> bool:
        """
        Check if difficulty should change based on P-Score thresholds.
        
        Thresholds:
        - Increase difficulty: P-Score ≥ +5
        - Decrease difficulty: P-Score ≤ -3
        - Reset P-Score to 0 after any transition
        
        Returns:
            bool: True if transition occurred
        """
        transition_occurred = False
        
        if self.p_score >= 5.0 and self.current_difficulty_index < len(self.difficulty_levels) - 1:
            # Increase difficulty
            self.current_difficulty_index += 1
            self.p_score = 0.0
            transition_occurred = True
            
        elif self.p_score <= -3.0 and self.current_difficulty_index > 0:
            # Decrease difficulty  
            self.current_difficulty_index -= 1
            self.p_score = 0.0
            transition_occurred = True
            
        return transition_occurred
    
    def get_status(self) -> dict:
        """Get current engine status for monitoring."""
        return {
            'p_score': round(self.p_score, 2),
            'difficulty': self.current_difficulty,
            'difficulty_index': self.current_difficulty_index,
            'increase_threshold': 5.0,
            'decrease_threshold': -3.0
        }