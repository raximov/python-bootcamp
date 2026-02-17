#!/usr/bin/env python3
"""
Task 4: Pascal's triangle
Output N first rows of Pascal's triangle by the given number N of rows.
Check the correctness of the input data.
"""

# Read input
input_str = input().strip()

# Check if input is a valid integer
try:
    n = int(input_str)
    
    # Check if it's a natural number (positive integer)
    if n <= 0:
        print("Natural number was expected")
    else:
        # Generate Pascal's triangle
        for i in range(n):
            row = [1]
            if i > 0:
                for j in range(1, i):
                    # Each element is sum of two elements above it
                    row.append(pascal_triangle[i-1][j-1] + pascal_triangle[i-1][j])
                row.append(1)
            
            if i == 0:
                pascal_triangle = [row]
            else:
                pascal_triangle.append(row)
            
            print(' '.join(map(str, row)))

except ValueError:
    print("Natural number was expected")
