#!/usr/bin/env python3
"""
Task 2: Palindrome
Determine whether the number is a palindrome or not.
Do not use strings. Negative numbers are not considered palindromes.
"""

# Read input number
num = int(input())

# Negative numbers are not palindromes
if num < 0:
    print(False)
else:
    # Reverse the number without using strings
    original = num
    reversed_num = 0
    
    while num > 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num = num // 10
    
    # Check if original equals reversed
    print(original == reversed_num)
