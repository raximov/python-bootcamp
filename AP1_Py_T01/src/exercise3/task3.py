#!/usr/bin/env python3
"""
Task 3: Figures
Process a square matrix of zeros and ones, count the number of "squares" and "circles".
"""

def flood_fill(matrix, visited, i, j, n):
    """Mark all connected cells and return their coordinates."""
    if i < 0 or i >= n or j < 0 or j >= n or visited[i][j] or matrix[i][j] == 0:
        return []
    
    visited[i][j] = True
    cells = [(i, j)]
    
    # Check all 4 directions
    cells.extend(flood_fill(matrix, visited, i+1, j, n))
    cells.extend(flood_fill(matrix, visited, i-1, j, n))
    cells.extend(flood_fill(matrix, visited, i, j+1, n))
    cells.extend(flood_fill(matrix, visited, i, j-1, n))
    
    return cells

def is_square(cells):
    """Check if the figure is a square."""
    if not cells:
        return False
    
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Square should be rectangular and completely filled
    if height != width:
        return False
    
    # Check if all cells in the rectangle are filled
    expected_cells = height * width
    return len(cells) == expected_cells

def is_circle(cells):
    """Check if the figure is a circle."""
    if not cells:
        return False
    
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Circle should be roughly square in bounding box
    if abs(height - width) > 1:
        return False
    
    # Calculate center
    center_row = (min_row + max_row) / 2
    center_col = (min_col + max_col) / 2
    
    # Check if it's not a perfect square (circles have less cells than filled rectangle)
    expected_cells = height * width
    if len(cells) == expected_cells:
        return False
    
    # Circle should have cells roughly equidistant from center
    return True

# Read matrix from input.txt
with open('input.txt', 'r') as f:
    lines = f.readlines()

matrix = []
for line in lines:
    row = list(map(int, line.strip().split()))
    matrix.append(row)

n = len(matrix)
visited = [[False] * n for _ in range(n)]

squares = 0
circles = 0

# Find all figures
for i in range(n):
    for j in range(n):
        if matrix[i][j] == 1 and not visited[i][j]:
            cells = flood_fill(matrix, visited, i, j, n)
            
            if len(cells) > 1:  # Figures contain more than one unit
                if is_square(cells):
                    squares += 1
                elif is_circle(cells):
                    circles += 1

print(f"{squares} {circles}")
