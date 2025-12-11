"""
Performance Tracker for Math Adventures
Tracks user performance metrics and session statistics.
"""

import time
from typing import List, Dict

class PerformanceTracker:
    """
    Tracks and analyzes user performance across the session.
    
    Maintains detailed logs of:
    - Response accuracy and timing
    - Difficulty transitions
    - P-Score evolution
    - Session statistics
    """
    
    def __init__(self):
        self.session_start = time.time()
        self.attempts = []
        self.difficulty_transitions = []
        
    def record_attempt(self, puzzle: dict, user_answer: int, response_time: float, 
                      is_correct: bool, engine_status: dict) -> None:
        """
        Record a single puzzle attempt with all relevant metrics.
        
        Args:
            puzzle: The puzzle dictionary from PuzzleGenerator
            user_answer: User's submitted answer
            response_time: Time taken to answer in seconds
            is_correct: Whether the answer was correct
            engine_status: Current adaptive engine status
        """
        attempt = {
            'timestamp': time.time() - self.session_start,
            'question': puzzle['question'],
            'correct_answer': puzzle['answer'],
            'user_answer': user_answer,
            'response_time': response_time,
            'is_correct': is_correct,
            'difficulty': puzzle['difficulty'],
            'p_score_after': engine_status['p_score'],
            'attempt_number': len(self.attempts) + 1
        }
        
        self.attempts.append(attempt)
    
    def record_difficulty_transition(self, old_difficulty: str, new_difficulty: str, 
                                   p_score: float, attempt_number: int) -> None:
        """Record when difficulty level changes."""
        transition = {
            'attempt_number': attempt_number,
            'from_difficulty': old_difficulty,
            'to_difficulty': new_difficulty,
            'trigger_p_score': p_score,
            'timestamp': time.time() - self.session_start
        }
        
        self.difficulty_transitions.append(transition)
    
    def get_session_summary(self) -> dict:
        """
        Generate comprehensive session statistics.
        
        Returns:
            dict: Complete performance analysis
        """
        if not self.attempts:
            return {'error': 'No attempts recorded'}
        
        total_attempts = len(self.attempts)
        correct_attempts = sum(1 for attempt in self.attempts if attempt['is_correct'])
        accuracy_rate = correct_attempts / total_attempts
        
        # Response time analysis
        response_times = [attempt['response_time'] for attempt in self.attempts]
        avg_response_time = sum(response_times) / len(response_times)
        fast_responses = sum(1 for rt in response_times if rt <= 5.0)
        
        # Difficulty distribution
        difficulty_counts = {}
        for attempt in self.attempts:
            diff = attempt['difficulty']
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        # P-Score progression
        p_score_progression = [attempt['p_score_after'] for attempt in self.attempts]
        final_p_score = p_score_progression[-1] if p_score_progression else 0
        
        return {
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'accuracy_rate': round(accuracy_rate * 100, 1),
            'avg_response_time': round(avg_response_time, 2),
            'fast_responses': fast_responses,
            'fast_response_rate': round((fast_responses / total_attempts) * 100, 1),
            'difficulty_distribution': difficulty_counts,
            'difficulty_transitions': len(self.difficulty_transitions),
            'final_p_score': round(final_p_score, 2),
            'p_score_range': {
                'min': round(min(p_score_progression), 2),
                'max': round(max(p_score_progression), 2)
            },
            'session_duration': round(time.time() - self.session_start, 1)
        }
    
    def get_recent_performance(self, last_n: int = 5) -> dict:
        """Analyze performance over the last N attempts."""
        if len(self.attempts) < last_n:
            recent_attempts = self.attempts
        else:
            recent_attempts = self.attempts[-last_n:]
        
        if not recent_attempts:
            return {'error': 'No recent attempts'}
        
        recent_correct = sum(1 for attempt in recent_attempts if attempt['is_correct'])
        recent_accuracy = recent_correct / len(recent_attempts)
        
        return {
            'attempts_analyzed': len(recent_attempts),
            'recent_accuracy': round(recent_accuracy * 100, 1),
            'recent_correct': recent_correct,
            'trend': 'improving' if recent_accuracy > 0.6 else 'struggling'
        }
    
    def print_detailed_log(self) -> None:
        """Print a detailed log of all attempts for debugging."""
        print("\n" + "="*80)
        print("DETAILED SESSION LOG")
        print("="*80)
        
        for attempt in self.attempts:
            status = "✓" if attempt['is_correct'] else "✗"
            print(f"#{attempt['attempt_number']:2d} [{attempt['difficulty']:6s}] "
                  f"{attempt['question']:15s} = {attempt['user_answer']:3d} {status} "
                  f"({attempt['response_time']:.1f}s) P-Score: {attempt['p_score_after']:+.1f}")
        
        print("\nDifficulty Transitions:")
        for trans in self.difficulty_transitions:
            print(f"  Attempt #{trans['attempt_number']}: "
                  f"{trans['from_difficulty']} → {trans['to_difficulty']} "
                  f"(P-Score: {trans['trigger_p_score']:+.1f})")
        
        print("="*80)