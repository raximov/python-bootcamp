#!/usr/bin/env python3
"""
Task 1: Scalar product
Calculate the scalar product of two vectors in three dimensional space.
"""

# Read first vector
vector1 = list(map(float, input().split()))

# Read second vector
vector2 = list(map(float, input().split()))

# Calculate scalar product
scalar_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

# Output result
print(scalar_product)
