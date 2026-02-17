#!/usr/bin/env python3
"""
Task 9: The derivative at a point
Calculate the derivative of a given polynomial at a given point.
"""

# Read degree and point
first_line = input().split()
n = int(first_line[0])
x = float(first_line[1])

# Read coefficients (from highest degree to lowest)
coefficients = []
for i in range(n + 1):
    coef = float(input())
    coefficients.append(coef)

# Calculate derivative at point x
# Derivative: if f(x) = a_n*x^n + a_(n-1)*x^(n-1) + ... + a_1*x + a_0
# Then f'(x) = n*a_n*x^(n-1) + (n-1)*a_(n-1)*x^(n-2) + ... + a_1

derivative_value = 0

for i in range(n):
    # Coefficient at degree (n-i)
    coef = coefficients[i]
    # Power in derivative is (n-i-1)
    power = n - i
    # Derivative coefficient is power * coef
    derivative_coef = power * coef
    # Evaluate at point x: derivative_coef * x^(power-1)
    derivative_value += derivative_coef * (x ** (power - 1))

# Print with 3 decimal places
print(f"{derivative_value:.3f}")
