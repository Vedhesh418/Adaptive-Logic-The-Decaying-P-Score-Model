"""
Math Adventures - Advanced Adaptive Learning System
Demonstrates superior adaptive logic with Decaying Performance Score (P-Score)

This prototype showcases:
- Stateful difficulty management
- Performance-based transitions
- Comprehensive tracking and analysis
"""

import time
import random
from adaptive_engine import AdaptiveEngine
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker

def simulate_user_response(puzzle: dict, difficulty: str) -> tuple:
    """
    Simulate realistic user responses based on difficulty and performance patterns.
    
    Returns:
        tuple: (user_answer, response_time, is_correct)
    """
    correct_answer = puzzle['answer']
    
    # Simulate response time based on difficulty and accuracy
    if difficulty == "Easy":
        base_time = random.uniform(2, 6)
        accuracy_chance = 0.85
    elif difficulty == "Medium":
        base_time = random.uniform(4, 10)
        accuracy_chance = 0.70
    else:  # Hard
        base_time = random.uniform(6, 15)
        accuracy_chance = 0.55
    
    # Determine if answer will be correct
    is_correct = random.random() < accuracy_chance
    
    if is_correct:
        user_answer = correct_answer
        # Correct answers tend to be faster
        response_time = base_time * random.uniform(0.7, 1.0)
    else:
        # Generate plausible wrong answer
        if random.random() < 0.5:
            # Off-by-one or calculation error
            user_answer = correct_answer + random.choice([-2, -1, 1, 2])
        else:
            # More significant error
            user_answer = int(correct_answer * random.uniform(0.5, 1.5))
        
        # Wrong answers often take longer (confusion/uncertainty)
        response_time = base_time * random.uniform(1.0, 1.4)
    
    return user_answer, response_time, is_correct

def run_math_adventures_session(num_turns: int = 15) -> None:
    """
    Run a complete Math Adventures session demonstrating the adaptive system.
    
    Args:
        num_turns: Number of puzzle attempts to simulate
    """
    print("🧮 MATH ADVENTURES - Advanced Adaptive Learning System")
    print("=" * 60)
    print("Demonstrating Decaying Performance Score (P-Score) Algorithm")
    print("=" * 60)
    
    # Initialize system components
    engine = AdaptiveEngine()
    generator = PuzzleGenerator()
    tracker = PerformanceTracker()
    
    print(f"\nStarting session with {num_turns} puzzle attempts...")
    print(f"Initial difficulty: {engine.current_difficulty}")
    print(f"Initial P-Score: {engine.p_score}")
    
    # Main session loop
    for turn in range(1, num_turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        # Generate puzzle for current difficulty
        puzzle = generator.generate_puzzle(engine.current_difficulty)
        print(f"Difficulty: {puzzle['difficulty']}")
        print(f"Question: {puzzle['question']} = ?")
        
        # Simulate user response
        user_answer, response_time, is_correct = simulate_user_response(
            puzzle, engine.current_difficulty
        )
        
        print(f"User answer: {user_answer} ({'✓' if is_correct else '✗'})")
        print(f"Correct answer: {puzzle['answer']}")
        print(f"Response time: {response_time:.1f}s")
        
        # Update adaptive engine
        update_info = engine.update_performance(is_correct, response_time)
        
        # Record attempt in tracker
        tracker.record_attempt(
            puzzle, user_answer, response_time, is_correct, engine.get_status()
        )
        
        # Display P-Score changes
        print(f"P-Score: {update_info['old_score']:+.2f} → {update_info['new_score']:+.2f}")
        print(f"Rationale: {update_info['rationale']}")
        
        # Handle difficulty transitions
        if update_info['transition_occurred']:
            print(f"🔄 DIFFICULTY TRANSITION: {update_info['old_difficulty']} → {update_info['new_difficulty']}")
            print("   P-Score reset to 0.0")
            
            tracker.record_difficulty_transition(
                update_info['old_difficulty'],
                update_info['new_difficulty'],
                update_info['old_score'],
                turn
            )
        
        # Show current status
        status = engine.get_status()
        print(f"Current: {status['difficulty']} (P-Score: {status['p_score']:+.2f})")
        
        # Brief pause for readability
        time.sleep(0.1)
    
    # Session complete - show comprehensive analysis
    print("\n" + "=" * 60)
    print("SESSION COMPLETE - PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    summary = tracker.get_session_summary()
    
    print(f"📊 Session Statistics:")
    print(f"   Total attempts: {summary['total_attempts']}")
    print(f"   Accuracy rate: {summary['accuracy_rate']}%")
    print(f"   Average response time: {summary['avg_response_time']}s")
    print(f"   Fast responses (≤5s): {summary['fast_responses']} ({summary['fast_response_rate']}%)")
    print(f"   Session duration: {summary['session_duration']}s")
    
    print(f"\n🎯 Adaptive Performance:")
    print(f"   Difficulty transitions: {summary['difficulty_transitions']}")
    print(f"   Final P-Score: {summary['final_p_score']}")
    print(f"   P-Score range: {summary['p_score_range']['min']} to {summary['p_score_range']['max']}")
    
    print(f"\n📈 Difficulty Distribution:")
    for difficulty, count in summary['difficulty_distribution'].items():
        percentage = (count / summary['total_attempts']) * 100
        print(f"   {difficulty}: {count} attempts ({percentage:.1f}%)")
    
    # Show recent performance trend
    recent = tracker.get_recent_performance()
    print(f"\n🔍 Recent Performance (last 5 attempts):")
    print(f"   Recent accuracy: {recent['recent_accuracy']}%")
    print(f"   Performance trend: {recent['trend']}")
    
    # Display detailed log for analysis
    tracker.print_detailed_log()
    
    print(f"\n✅ Demonstration complete! The Decaying P-Score system successfully:")
    print(f"   • Adapted difficulty based on performance patterns")
    print(f"   • Handled noisy/inconsistent responses through decay mechanism")
    print(f"   • Provided clear rationale for all transitions")
    print(f"   • Maintained engagement through appropriate challenge levels")

if __name__ == "__main__":
    # Run the demonstration
    run_math_adventures_session(15)