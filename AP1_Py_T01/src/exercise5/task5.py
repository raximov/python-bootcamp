#!/usr/bin/env python3
"""
Task 5: String to number conversion
Convert a string to a real number without using float() function.
Multiply the resulting real number by 2 and print with 3 digits after the dot.
"""

def string_to_float(s):
    """Convert string to float manually."""
    s = s.strip()
    
    # Handle sign
    sign = 1
    start = 0
    if s[0] in ('+', '-'):
        if s[0] == '-':
            sign = -1
        start = 1
    
    # Split by decimal point
    if '.' in s:
        parts = s[start:].split('.')
        if len(parts) != 2:
            raise ValueError("Invalid format")
        integer_part = parts[0] if parts[0] else '0'
        decimal_part = parts[1]
    else:
        integer_part = s[start:]
        decimal_part = '0'
    
    # Check if parts contain only digits
    if not integer_part.isdigit() or not decimal_part.isdigit():
        raise ValueError("Invalid format")
    
    # Convert integer part
    result = 0
    for digit in integer_part:
        result = result * 10 + int(digit)
    
    # Convert decimal part
    decimal_value = 0
    divisor = 1
    for digit in decimal_part:
        divisor *= 10
        decimal_value = decimal_value * 10 + int(digit)
    
    result += decimal_value / divisor
    
    return sign * result

# Read input
input_str = input().strip()

try:
    # Convert string to float
    number = string_to_float(input_str)
    
    # Multiply by 2
    result = number * 2
    
    # Print with 3 digits after decimal point
    print(f"{result:.3f}")
    
except (ValueError, IndexError):
    print("Invalid input format")
