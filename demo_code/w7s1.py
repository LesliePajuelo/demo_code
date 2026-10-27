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
"""