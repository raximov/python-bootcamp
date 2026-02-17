#!/usr/bin/env python3
"""
Task 6: Movies
Join two lists of movies sorted by the year field.
Input and output data is in JSON format.
"""

import json
import os

# Check if file exists and is not empty
if not os.path.exists('input.txt'):
    print("File not found")
elif os.path.getsize('input.txt') == 0:
    print("Empty file")
else:
    try:
        # Read data from input.txt
        with open('input.txt', 'r') as f:
            data = json.load(f)
        
        # Get the two lists
        list1 = data.get('list1', [])
        list2 = data.get('list2', [])
        
        # Merge the two sorted lists
        merged_list = []
        i, j = 0, 0
        
        while i < len(list1) and j < len(list2):
            if list1[i]['year'] <= list2[j]['year']:
                merged_list.append(list1[i])
                i += 1
            else:
                merged_list.append(list2[j])
                j += 1
        
        # Add remaining elements
        while i < len(list1):
            merged_list.append(list1[i])
            i += 1
        
        while j < len(list2):
            merged_list.append(list2[j])
            j += 1
        
        # Create output structure
        output = {"list0": merged_list}
        
        # Print as JSON with proper formatting
        print(json.dumps(output, indent=2))
    
    except json.JSONDecodeError:
        print("Invalid JSON format")
    except KeyError:
        print("Invalid data structure")
    except Exception as e:
        print(f"Error: {str(e)}")
