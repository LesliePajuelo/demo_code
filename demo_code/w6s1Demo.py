from collections import deque

def get_quest_order(numQuests: int, prerequisites: list[list[int]]) -> list[int]:
    # Initialize adjacency list and in-degree array
    adj = {i: [] for i in range(numQuests)}
    in_degree = [0] * numQuests
    
    # Build the graph
    for quest, prereq in prerequisites:
        adj[prereq].append(quest)
        in_degree[quest] += 1
        
    # Initialize the queue
    queue = deque([i for i in range(numQuests) if in_degree[i] == 0])

    # Initialize result list
    order = []
    

    # Return result (Check for cycles)
    return order if len(order) == numQuests else []


assert get_quest_order(4, [[1, 0], [2, 1], [3, 2]]) == [0, 1, 2, 3], "Failed standard directed acyclic graph"

assert get_quest_order(2, [[1, 0], [0, 1]]) == [], "Failed cycle detection (should return empty list)"

assert get_quest_order(3, []) == [0, 1, 2], "Failed graph with no dependencies"


import heapq

def minimum_effort_path(heights: list[list[int]]) -> int:
    #  Initialize dimensions and movement offsets 
    total_rows, total_cols = len(heights), len(heights[0])
    row_col_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    #  Initialize min_recorded_efforts array and starting point 
    min_recorded_efforts = [[float('inf')] * total_cols for _ in range(total_rows)]
    min_recorded_efforts[0][0] = 0
    
    #  Initialize priority queue (effort, row, col) 
    path_queue = [(0, 0, 0)]
    
    # Core Dijkstra Loop
 
        #  Look at the grid (Neighbors & Updating) 
        for row_offset, col_offset in row_col_offsets:
            neighbor_row, neighbor_col = current_row + row_offset, current_col + col_offset
            
            if 0 <= neighbor_row < total_rows and 0 <= neighbor_col < total_cols:
                effort_to_neighbor = max(current_effort, abs(heights[current_row][current_col] - heights[neighbor_row][neighbor_col]))
                
                if effort_to_neighbor < min_recorded_efforts[neighbor_row][neighbor_col]:
                    min_recorded_efforts[neighbor_row][neighbor_col] = effort_to_neighbor
                    heapq.heappush(path_queue, (effort_to_neighbor, neighbor_row, neighbor_col))
                    
    #  Fallback return 
    return 0

# 1. Has Values (Standard grid): Optimal path avoids the '8' in the middle. 
# Path goes down the left side and across the bottom: 1 -> 3 -> 5 -> 3 -> 5 (max difference is 2).
assert minimum_effort_path([
    [1, 2, 2], 
    [3, 8, 2], 
    [5, 3, 5]
]) == 2, "Failed standard grid"

# 2. "Doesn't" (1x1 grid): Start and destination are the exact same cell.
assert minimum_effort_path([[5]]) == 0, "Failed 1x1 grid (effort should be 0)"

# 3. Edge Case (Snake path required): Must travel completely backwards (left/up) 
# to stay in the valleys of '1's and avoid the walls of '10's.
assert minimum_effort_path([
    [1, 10, 10], 
    [1, 10, 10], 
    [1,  1,  1]
]) == 0, "Failed flat path around obstacles"