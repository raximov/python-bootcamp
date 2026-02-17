#!/usr/bin/env python3
"""
Task 7: A robot
The robot moves down or right collecting maximum coins.
Use dynamic programming to find the optimal path.
"""

# Read dimensions
n, m = map(int, input().split())

# Read the field
field = []
for i in range(n):
    row = list(map(int, input().split()))
    field.append(row)

# Create DP table
dp = [[0] * m for _ in range(n)]

# Initialize first cell
dp[0][0] = field[0][0]

# Fill first row (can only come from left)
for j in range(1, m):
    dp[0][j] = dp[0][j-1] + field[0][j]

# Fill first column (can only come from top)
for i in range(1, n):
    dp[i][0] = dp[i-1][0] + field[i][0]

# Fill rest of the table
for i in range(1, n):
    for j in range(1, m):
        # Take maximum of coming from top or from left
        dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + field[i][j]

# The answer is in bottom-right corner
print(dp[n-1][m-1])
