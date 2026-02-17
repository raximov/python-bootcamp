#!/usr/bin/env python3
"""
Task 10: Machines
Select two machines with same year, minimal cost, and required total running time.
"""

# Read input
try:
    first_line = input().split()
    n = int(first_line[0])
    required_time = int(first_line[1])
    
    # Read machines data
    machines = []
    for _ in range(n):
        line = input().split()
        year = int(line[0])
        cost = int(line[1])
        time = int(line[2])
        machines.append((year, cost, time))
    
    # Group machines by year
    machines_by_year = {}
    for year, cost, time in machines:
        if year not in machines_by_year:
            machines_by_year[year] = []
        machines_by_year[year].append((cost, time))
    
    # Find the best pair
    best_cost = float('inf')
    found = False
    
    for year, machine_list in machines_by_year.items():
        # Try all pairs of machines with the same year
        for i in range(len(machine_list)):
            for j in range(i + 1, len(machine_list)):
                cost1, time1 = machine_list[i]
                cost2, time2 = machine_list[j]
                
                # Check if total time matches
                if time1 + time2 == required_time:
                    total_cost = cost1 + cost2
                    if total_cost < best_cost:
                        best_cost = total_cost
                        found = True
    
    if found:
        print(best_cost)
    else:
        print("No solution found")

except (ValueError, IndexError):
    print("Invalid input format")
