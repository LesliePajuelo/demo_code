""""
Problem statement

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

"""


'''
SPEAKER NOTES:
"Let's build Union Find, also known as Disjoint Set, for the power grid.
Each substation is a node. Each grid component is a group.
We need to track 'parent' of each substation.
Initially, every substation is its own parent, meaning it's in its own isolated grid component.
We also track 'rank' to keep trees shallow."
'''
class UnionFind:
    def __init__(self, n):
        # "Parent array: each substation points to itself."
        self.parent = [i for i in range(n)]
        # "Rank array: initialized with 0s to optimize union later."
        self.rank = [0] * n

# --- SECTION 2: FIND OPERATION ---
    '''
    SPEAKER NOTES (Pseudocode & Explanation):
    "First, 'find' operation. Goal: find root substation of the grid component.
    Pseudocode:
    1. If current substation is not its own parent, it's not root.
    2. Recursively call find on its parent.
    3. Set current substation's parent directly to root (Path Compression).
    4. Return root."
    '''
    def find(self, x):
        # "If x is not root..."
        if self.parent[x] != x:
            # "...recursively find root, point x directly to it."
            self.parent[x] = self.find(self.parent[x])
        # "Return root."
        return self.parent[x]

# --- SECTION 3: UNION OPERATION ---
    '''
    SPEAKER NOTES (Pseudocode & Explanation):
    "Next, 'union'. Goal: build a transmission line and merge two grid components.
    Pseudocode:
    1. Find root of origin substation and root of destination substation.
    2. If roots are same, they are already on the same grid component. Done.
    3. If different, attach root of shorter tree under root of taller tree (Union by Rank).
    4. If same height, pick one as new root, increase its rank."
    '''
    def union(self, x, y):
        # "Find roots of both substations."
        root_x = self.find(x)
        root_y = self.find(y)

        # "If same component, nothing to do. Duplicate or self-loop line."
        if root_x == root_y:
            return False

        # "Union by Rank: attach smaller tree under taller tree."
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            # "If same height, attach y to x, increment rank of x."
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

# --- SECTION 4: CONNECTIVITY QUERY ---
    '''
    SPEAKER NOTES:
    "Query: two substations are connected if they share the same root."
    '''
    def connected(self, x, y):
        return self.find(x) == self.find(y)

# --- SECTION 5: DEMONSTRATION ---
    '''
    SPEAKER NOTES:
    "Let's run 6-substation example.
    For each operation, build the line, then query connectivity.
    Expected results: [False, True, False, True, True]."
    '''
if __name__ == "__main__":
    # "Create Disjoint Set for 6 substations (0 to 5)."
    n = 6
    # "Operations: (origin, destination, query_a, query_b)."
    grid_operations = [
        (0, 1, 0, 2),  # "Build line (0,1), query (0,2): False."
        (1, 2, 0, 2),  # "Build line (1,2), query (0,2): True."
        (3, 4, 3, 5),  # "Build line (3,4), query (3,5): False."
        (4, 5, 3, 5),  # "Build line (4,5), query (3,5): True."
        (0, 3, 0, 5),  # "Build line (0,3), query (0,5): True."
    ]

    ds = UnionFind(n)
    results = []
    for origin, destination, query_a, query_b in grid_operations:
        # "Build the transmission line."
        ds.union(origin, destination)
        # "Query whether the two substations share a grid component."
        results.append(ds.connected(query_a, query_b))
        print(f"Build ({origin},{destination}), query ({query_a},{query_b}):", results[-1])
        print("Parents:", ds.parent)

    print("Results:", results)
    assert results == [False, True, False, True, True], "Unexpected grid connectivity results!"
    print("All tests passed successfully!")
