"""
In regional power grid management, high-voltage transmission lines are constructed 
  sequentially between electrical substations. System operators need an efficient way 
  to monitor grid connectivity and verify whether power can flow between specific remote 
  substations across the integrated network as new lines come online.

Inputs:
- n: number of electrical substations (0 to n-1)
- operations: sequence of tuples (substation_origin, substation_destination, grid_query_node_a, grid_query_node_b)
  - A high-voltage transmission line is built between substation_origin and substation_destination.
  - Immediately followed by a query checking if grid_query_node_a and grid_query_node_b belong to the same grid component.

Happy Path Test:
- 6 substations (0-5). 
- Operations: build line (0,1) & query (0,2), build line (1,2) & query (0,2), etc.

Edge Cases:
- Single substation grid (n=1, no transmission lines, trivial queries).
- Isolated subnets with no transmission lines built.
- Duplicate line installations and feedback loops (self-loops).

==========================================
MATCH
==========================================
Pattern: Dynamic Connectivity / Component Membership.
- Dijkstra's Algorithm finds shortest path weighted distances.
  - Graph Type: Directed or undirected graph with non-negative edge weights.
  - Best Match: Single-source shortest path problems requiring distance accumulation.
- Disjoint Set Union (DSU / Union-Find) maintains disjoint sets in near-constant time.
  - Graph Type: Undirected graph used for dynamic connectivity.
  - Best Match: Problems where edges are added incrementally and you need to query 
    component membership without edge weights.

==========================================
PLAN: Dijkstra Approach
==========================================
- Initialize adjacency list dictionary to store power grid network structure.
- Initialize tracking array to store query boolean results for each step.
- Loop through every incoming transmission line and query operation in input sequence.
  - Extract origin substation_origin, destination substation_destination, and query nodes grid_query_node_a, grid_query_node_b.
  - Append bidirectional power line substation_destination to adjacency list grid_network[substation_origin] with weight.
  - Initialize min-heap priority queue for Dijkstra containing starting tuple (0, grid_query_node_a).
  - Initialize distances hash map setting grid_distances[grid_query_node_a] = 0 and tracking visited substations.
  - While priority queue is not empty, pop substation with current minimum accumulated weight.
    - If popped substation matches target query node grid_query_node_b, record connected and break.
    - Iterate through all neighboring substations and line weights connected to current substation.
      - Compute tentative new distance by adding current path weight to line weight.
      - If new distance is strictly smaller than recorded distance, update and push to queue.
  - Append final computed reachability boolean status to results list.

==========================================
PLAN: DSU Approach
==========================================
- Instantiate DSU class with n substations, setting each substation's initial parent pointer to itself.
- Define find(substation) method to locate root representative of substation.
  - Inside find(substation), if substation is not its own parent, recursively update substation_grid_roots[substation] 
    to point directly to root (path compression).
- Define union(substation_a, substation_b) method to merge sets containing substation_a and substation_b.
  - Inside union(substation_a, substation_b), find root representatives for both substations:
    - Use the find method to locate root_a for substation_a.
    - Use the find method to locate root_b for substation_b.
  - Connect one root to the other if distinct roots are found.
- Initialize results tracking list for storing dynamic connectivity query outcomes.
- Loop through every incoming transmission line and query operation in input sequence.
  - Call substation_dsu.union(substation_origin, substation_destination) to dynamically merge grid components.
  - Evaluate connectivity by checking if substation_dsu.find(grid_query_node_a) == substation_dsu.find(grid_query_node_b).
  - Append resulting boolean value to results list and return final collection.
"""
import heapq
from collections import defaultdict, deque

# ==========================================
# IMPLEMENTATION: Dijkstra Approach
# ==========================================

def dijkstra_smart_grid_connectivity(n, grid_operations):
    # Initialize adjacency list matching PLAN step (store power grid structure)
    grid_network = {substation: [] for substation in range(n)}
    # Track connectivity results for each step
    results = []
    
    # Iterate through each transmission line construction and query matching PLAN step
    for substation_origin, substation_destination, grid_query_node_a, grid_query_node_b in grid_operations:
        # Add undirected transmission line to network matching PLAN step
        grid_network[substation_origin].append((substation_destination, 1))
        # Add reverse transmission line for bidirectional grid matching PLAN step
        grid_network[substation_destination].append((substation_origin, 1))
        
        # Run Dijkstra reachability from grid_query_node_a matching PLAN step
        pq = [(0, grid_query_node_a)]
        grid_distances = {grid_query_node_a: 0}
        visited_substations = set()
        connected = False
        
        # Standard Dijkstra shortest path loop matching PLAN step
        while pq:
            current_distance, current_substation = heapq.heappop(pq)
            
            if current_substation in visited_substations:
                continue
            visited_substations.add(current_substation)
            
            # Check if target grid_query_node_b is reached matching PLAN step
            if current_substation == grid_query_node_b:
                connected = True
                break
                
            # Iterate through neighboring substations matching PLAN step
            for neighbor_substation, line_weight in grid_network[current_substation]:
                tentative_distance = current_distance + line_weight
                
                # Update shortest path distance matching PLAN step
                if neighbor_substation not in grid_distances or tentative_distance < grid_distances[neighbor_substation]:
                    grid_distances[neighbor_substation] = tentative_distance
                    heapq.heappush(pq, (tentative_distance, neighbor_substation))
                    
        # Append connectivity status to results matching PLAN step
        results.append(connected)
        
    # Return all query results matching PLAN
    return results

# ==========================================
# IMPLEMENTATION: DSU Approach
# ==========================================

class SubstationDisjointSetUnion:
    def __init__(self, n):
        # Initialize parent dict where each substation is its own parent matching PLAN step
        self.substation_grid_roots = {substation: substation for substation in range(n)}
        
    def find(self, substation):
        # Check if substation is not its own root matching PLAN step
        if self.substation_grid_roots[substation] != substation:
            # Recursively find root and compress path matching PLAN step
            self.substation_grid_roots[substation] = self.find(self.substation_grid_roots[substation])
        # Return root representative matching PLAN step
        return self.substation_grid_roots[substation]
        
    def union(self, substation_a, substation_b):
        # Find root of set containing substation_a matching PLAN step
        root_a = self.find(substation_a)
        # Find root of set containing substation_b matching PLAN step
        root_b = self.find(substation_b)
        # Check if roots are distinct matching PLAN step
        if root_a != root_b:
            # Merge set a into set b matching PLAN step
            self.substation_grid_roots[root_a] = root_b
            # Return True indicating successful merge matching PLAN step
            return True
        # Return False if already in same set matching PLAN step
        return False

def dsu_smart_grid_connectivity(n, grid_operations):
    # Instantiate DSU object with n substations matching PLAN
    substation_dsu = SubstationDisjointSetUnion(n)
    # Track connectivity results for each step matching PLAN
    results = []
    
    # Iterate through each transmission line construction and query matching PLAN
    for substation_origin, substation_destination, grid_query_node_a, grid_query_node_b in grid_operations:
        # Union the two substations to build transmission line matching PLAN
        substation_dsu.union(substation_origin, substation_destination)
        # Check if query substations share the same root matching PLAN step
        is_connected = substation_dsu.find(grid_query_node_a) == substation_dsu.find(grid_query_node_b)
        # Append query result matching PLAN
        results.append(is_connected)
        
    # Return query results matching PLAN
    return results

# ==========================================
# EVALUATION & TEST EXECUTION
# ==========================================

if __name__ == "__main__":
    # Define test scenario: 6 substations (0 to 5)
    n = 6
    # Operations: (substation_origin, substation_destination, grid_query_node_a, grid_query_node_b)
    grid_operations = [
        (0, 1, 0, 2),  # Build line (0,1), check if 0 and 2 connected (False)
        (1, 2, 0, 2),  # Build line (1,2), check if 0 and 2 connected (True)
        (3, 4, 3, 5),  # Build line (3,4), check if 3 and 5 connected (False)
        (4, 5, 3, 5),  # Build line (4,5), check if 3 and 5 connected (True)
        (0, 3, 0, 5),  # Build line (0,3), check if 0 and 5 connected (True)
    ]
    
    print("Running Dijkstra Smart Grid Connectivity:")
    dijkstra_res = dijkstra_smart_grid_connectivity(n, grid_operations)
    print(f"Results: {dijkstra_res}")
    
    print("\nRunning DSU Smart Grid Connectivity:")
    dsu_res = dsu_smart_grid_connectivity(n, grid_operations)
    print(f"Results: {dsu_res}")
    
    assert dijkstra_res == dsu_res, "Mismatch between Dijkstra and DSU results!"
    print("\nAll tests passed successfully!")