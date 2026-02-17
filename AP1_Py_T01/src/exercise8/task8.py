#!/usr/bin/env python3
"""
Task 8: Different numbers
Count the number of different numbers entered.
"""

# Read the count of numbers
n = int(input())

# Use a set to store unique numbers
unique_numbers = set()

# Read n numbers
for _ in range(n):
    num = int(input())
    unique_numbers.add(num)

# Print the count of unique numbers
print(len(unique_numbers))
