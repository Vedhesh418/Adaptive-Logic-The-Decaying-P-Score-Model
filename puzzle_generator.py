"""
Puzzle Generator for Math Adventures
Generates arithmetic problems based on difficulty level.
"""

import random

class PuzzleGenerator:
    """
    Generates math puzzles with difficulty-appropriate complexity.
    
    Difficulty scaling:
    - Easy: Single-digit addition/subtraction
    - Medium: Two-digit operations, simple multiplication
    - Hard: Multi-step problems, larger numbers
    """
    
    def __init__(self):
        self.operations = {
            'Easy': self._generate_easy_puzzle,
            'Medium': self._generate_medium_puzzle, 
            'Hard': self._generate_hard_puzzle
        }
    
    def generate_puzzle(self, difficulty: str) -> dict:
        """
        Generate a math puzzle for the specified difficulty.
        
        Args:
            difficulty: One of 'Easy', 'Medium', 'Hard'
            
        Returns:
            dict: Contains 'question', 'answer', and 'difficulty'
        """
        if difficulty not in self.operations:
            raise ValueError(f"Unknown difficulty: {difficulty}")
            
        return self.operations[difficulty]()
    
    def _generate_easy_puzzle(self) -> dict:
        """Generate easy single-digit arithmetic."""
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            question = f"{a} + {b}"
            answer = a + b
        else:  # subtraction
            a = random.randint(5, 9)  # Ensure positive result
            b = random.randint(1, a)
            question = f"{a} - {b}"
            answer = a - b
            
        return {
            'question': question,
            'answer': answer,
            'difficulty': 'Easy'
        }
    
    def _generate_medium_puzzle(self) -> dict:
        """Generate medium two-digit operations."""
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            question = f"{a} + {b}"
            answer = a + b
        elif operation == '-':
            a = random.randint(20, 99)
            b = random.randint(10, a)
            question = f"{a} - {b}"
            answer = a - b
        else:  # multiplication
            a = random.randint(2, 9)
            b = random.randint(2, 12)
            question = f"{a} × {b}"
            answer = a * b
            
        return {
            'question': question,
            'answer': answer,
            'difficulty': 'Medium'
        }
    
    def _generate_hard_puzzle(self) -> dict:
        """Generate hard multi-step or complex problems."""
        puzzle_type = random.choice(['multi_step', 'large_numbers', 'division'])
        
        if puzzle_type == 'multi_step':
            # Problems like: (a + b) × c
            a = random.randint(5, 15)
            b = random.randint(5, 15)
            c = random.randint(2, 8)
            question = f"({a} + {b}) × {c}"
            answer = (a + b) * c
            
        elif puzzle_type == 'large_numbers':
            # Three-digit addition/subtraction
            operation = random.choice(['+', '-'])
            if operation == '+':
                a = random.randint(100, 500)
                b = random.randint(100, 500)
                question = f"{a} + {b}"
                answer = a + b
            else:
                a = random.randint(200, 999)
                b = random.randint(100, a)
                question = f"{a} - {b}"
                answer = a - b
                
        else:  # division
            # Division with whole number results
            quotient = random.randint(5, 20)
            divisor = random.randint(3, 12)
            dividend = quotient * divisor
            question = f"{dividend} ÷ {divisor}"
            answer = quotient
            
        return {
            'question': question,
            'answer': answer,
            'difficulty': 'Hard'
        }