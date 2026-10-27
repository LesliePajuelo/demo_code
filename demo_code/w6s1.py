"""
PLANS

Directed Acyclic Graph (DAG) - Topological Sort via Kahn's Algorithm

* Init an in_degree hash map (frequency map) with a value of zero for every vertex in the graph.
* Init an adjacency list mapping every vertex to an empty list.
* Iterate through the input edges (where edge is u -> v):
  * Append v to the adjacency list of u.
  * Increment the in_degree of v by one.
* Init a queue and push all vertices that have an in_degree of zero (the starting nodes with no prerequisites).
* Init an empty result list to store the topological order.
* While the queue is not empty:
  * Pop the current_node from the front of the queue.
  * Append current_node to the result list.
  * Iterate through each neighbor in the adjacency list of current_node:
    * Decrement the in_degree of the neighbor by one.
    * If the in_degree of the neighbor drops to zero, push the neighbor to the back of the queue.
* Compare the length of the result list to the total number of vertices:
  * If they match, return the result list (a valid DAG exists).
  * If they do not match, return an error or empty sequence (a cycle exists, meaning it is not a valid DAG).

Dijkstra’s Algorithm using a Min-Heap (Shortest Path / Minimax Path)

* Init a costs or distances hash map or two-dimensional array, setting the cost to reach all vertices to infinity.
* Set the cost of the start_node to zero.
* Init a min_heap priority queue and push the starting tuple: (zero, start_node) representing (current_cost, node).
* While the min_heap is not empty:
  * Pop the smallest (current_cost, current_node) tuple from the min_heap.
  * Optional Target Check: If current_node is the destination, immediately return current_cost.
  * Stale State Check: If current_cost is greater than the recorded cost of current_node, continue to the next iteration to skip outdated paths.
  * Iterate through each neighbor and its corresponding edge_weight from the adjacency list of current_node:
    * Calculate the new_cost to reach the neighbor.
      * For Standard Dijkstra's: new_cost equals current_cost plus edge_weight.
      * For Minimax Dijkstra's: new_cost equals the maximum of current_cost and edge_weight.
    * If new_cost is less than the recorded cost of the neighbor:
      * Update the recorded cost of the neighbor to new_cost.
      * Push the updated tuple (new_cost, neighbor) into the min_heap.
* Return the full costs structure, or the specific cost of the target_node if returning a single destination.
"""


"""
PROBLEM 1: The 100% Speedrun (Quest Completion Order)

UNDERSTAND and MATCH:
- Say: Before we type a single character, what do we need to ask our Game Designer?
- Clarifications:
  - Can a quest have multiple prerequisites? (Yes)
  - Can there be cycles? (If yes, it's a bug)
  - Are all quests connected? (Not necessarily)
- Match: We see "order" and "dependencies." This is a topological sort on a directed acyclic graph (DAG).

PLAN:
- List out the initial state for a simple example: 3 Quests, Prereqs: [[1,0], [2, 1]]
- Count in-degrees (How many prerequisites per quest?) – 2
  - Start with quests that have 0 in-degree.
  - When we "finish" a quest, "unlock" its children.
- Draw the nodes 0, 1, and 2. Draw arrows. Mark the in-degrees: 0:0, 1:1, 2:1

IMPLEMENT:
- Write the function signature.
- Build the graph – convert those raw pairs into an adjacency list so we can actually traverse it.
- Say: Why use a queue? Because it lets us process quests in the order they become available (BFS style).

REVIEW and EVALUATE:
- Trace the code with the example [0 -> 1 -> 2]
  - Queue starts with 0. Pop 0. Neighbor 1's in-degree drops to 0. Add 1 to queue…
- Say: We visit every quest (V) and every prerequisite (E). Complexity? O(V + E). Space is O(V) for the queue and result list.
"""
from collections import deque
"""
PLAN:
1. init an adjacency list `adj` and an `in_degree` array of size `numQuests` to track dependencies.
2. Iterate through `prerequisites` to build the graph (directed edges from `prereq` to `quest`) and count in-degrees.
3. init a `queue` with all quests that have an in-degree of 0 (no prerequisites).
4. init a result list `order` to store the completion sequence.
5. While the `queue` is not empty:
6.     Pop the `current` quest from the left of the queue.
7.     Append `current` to the `order` list.
8.     Iterate through all `neighbor` quests dependent on `current`:
9.         Decrement the neighbor's `in_degree` by 1.
10.        If the neighbor's `in_degree` becomes 0, append it to the queue.
11. If the length of `order` equals `numQuests`, return `order` (valid DAG); otherwise return `[]` (cycle detected).

assert get_quest_order(4, [[1, 0], [2, 1], [3, 2]]) == [0, 1, 2, 3], "Failed standard directed acyclic graph"

assert get_quest_order(2, [[1, 0], [0, 1]]) == [], "Failed cycle detection (should return empty list)"

assert get_quest_order(3, []) == [0, 1, 2], "Failed graph with no dependencies"

"""

from collections import deque

def get_quest_order(numQuests: int, prerequisites: list[list[int]]) -> list[int]:
    # 1. init an adjacency list adj and an in_degree array of size numQuests to track dependencies.
    adj = {i: [] for i in range(numQuests)}
    in_degree = [0] * numQuests
    
    # 2. Iterate through prerequisites to build the graph (directed edges from prereq to quest) and count in-degrees.
    for quest, prereq in prerequisites:
        adj[prereq].append(quest)
        in_degree[quest] += 1
        
    # 3. init a queue with all quests that have an in-degree of 0 (no prerequisites).
    queue = deque([i for i in range(numQuests) if in_degree[i] == 0])
    
    # 4. init a result list order to store the completion sequence.
    order = []
    
    # 5. While the queue is not empty:
    while queue:
        # 6.     Pop the current quest from the left of the queue.
        current = queue.popleft()
        
        # 7.     Append current to the order list.
        order.append(current)
        
        # 8.     Iterate through all neighbor quests dependent on current:
        for neighbor in adj[current]:
            # 9.         Decrement the neighbor's in_degree by 1.
            in_degree[neighbor] -= 1
            
            # 10.        If the neighbor's in_degree becomes 0, append it to the queue.
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 11. If the length of order equals numQuests, return order (valid DAG); otherwise return [] (cycle detected).
    return order if len(order) == numQuests else []

# Test it:
# print(get_quest_order(3, [[1,0], [2,1]])) # Output: [0, 1, 2]


"""
 Path with Minimum Effort (Minimax Path)
 Prompt:
    https://gist.github.com/jamjamgobambam/c34b0bb6ec6f13241c13ca5d8bee46f0

UNDERSTAND:
Problem: Find path from (0,0) to (rows-1, cols-1) in grid `heights` minimizing effort.
Effort is maximum absolute difference in heights between consecutive cells.
Inputs: 2D integer array `heights`.
Outputs: Integer minimum path effort.
Constraints: Moves restricted up, down, left, right.

MATCH:
Problem Words: "situated in top-left... travel to bottom-right", "minimizes... effort".
Pattern Identification: Grid movement defines graph adjacency. "Minimizes" path cost signals 
shortest-path graph algorithm. Path cost is maximum edge weight, not sum.
Algorithm Chosen: Modified Dijkstra's Algorithm using Min-Heap (Minimax Path).

PLAN:
# PLAN:
# 1. init total_rows, total_cols, and row_col_offsets array.
# 2. init min_recorded_efforts 2D array with infinity, min_recorded_efforts[0][0] = 0.
# 3. init path_queue with (0, 0, 0) -> (current_effort, current_row, current_col).
# 4. While path_queue:
# 5.     Pop current_effort, current_row, current_col.
# 6.     If at destination, return current_effort.
# 7.     If current_effort > min_recorded_efforts[current_row][current_col], continue.
# 8.     For row_offset, col_offset in row_col_offsets:
# 9.         Calculate neighbor_row, neighbor_col.
# 10.        If bounds check passes:
# 11.            Calculate effort_to_neighbor = max(current_effort, abs(heights[current_row][current_col] - heights[neighbor_row][neighbor_col])).
# 12.            If effort_to_neighbor < min_recorded_efforts[neighbor_row][neighbor_col]:
# 13.                Update min_recorded_efforts[neighbor_row][neighbor_col] = effort_to_neighbor.
# 14.                Push (effort_to_neighbor, neighbor_row, neighbor_col) to path_queue.

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
"""
import heapq

def minimum_effort_path(heights: list[list[int]]) -> int:
    # 1. init total_rows, total_cols, and row_col_offsets array.
    total_rows, total_cols = len(heights), len(heights[0])
    row_col_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # 2. init min_recorded_efforts 2D array with infinity, min_recorded_efforts[0][0] = 0.
    min_recorded_efforts = [[float('inf')] * total_cols for _ in range(total_rows)]
    min_recorded_efforts[0][0] = 0
    
    # 3. init path_queue with (0, 0, 0) -> (current_effort, current_row, current_col).
    path_queue = [(0, 0, 0)]
    
    #########################
    # Core Dijkstra Loop !!!
    #######################
    # 4. While path_queue:
    while path_queue:
        # 5.     Pop current_effort, current_row, current_col.
        current_effort, current_row, current_col = heapq.heappop(path_queue)
        
        # 6.     If at destination, return current_effort.
        if current_row == total_rows - 1 and current_col == total_cols - 1:
            return current_effort
            
        # 7.     If current_effort > min_recorded_efforts[current_row][current_col], continue.
        if current_effort > min_recorded_efforts[current_row][current_col]:
            continue
        
        #########################
        # END Core Dijkstra Loop !!!
        #######################
        
          #  Look at the grid (Neighbors & Updating) 
        # 8.     For row_offset, col_offset in row_col_offsets:
        for row_offset, col_offset in row_col_offsets:
            # 9.         Calculate neighbor_row, neighbor_col.
            neighbor_row, neighbor_col = current_row + row_offset, current_col + col_offset
            
            # 10.If bounds check passes:
            if 0 <= neighbor_row < total_rows and 0 <= neighbor_col < total_cols:
                # 11. Calculate effort_to_neighbor.
                effort_to_neighbor = max(current_effort, abs(heights[current_row][current_col] - heights[neighbor_row][neighbor_col]))
                
                # 12. If effort_to_neighbor < min_recorded_efforts[neighbor_row][neighbor_col]:
                if effort_to_neighbor < min_recorded_efforts[neighbor_row][neighbor_col]:
                    # 13. Update min_recorded_efforts[neighbor_row][neighbor_col] = effort_to_neighbor.
                    min_recorded_efforts[neighbor_row][neighbor_col] = effort_to_neighbor
                    
                    # 14. Push (effort_to_neighbor, neighbor_row, neighbor_col) to path_queue.
                    heapq.heappush(path_queue, (effort_to_neighbor, neighbor_row, neighbor_col))
                    
    return 0




assert get_quest_order(4, [[1, 0], [2, 1], [3, 2]]) == [0, 1, 2, 3], "Failed standard directed acyclic graph"

assert get_quest_order(2, [[1, 0], [0, 1]]) == [], "Failed cycle detection (should return empty list)"

assert get_quest_order(3, []) == [0, 1, 2], "Failed graph with no dependencies"






