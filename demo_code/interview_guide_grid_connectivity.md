# UMPIRE Interview Guide — Power Grid Connectivity

## U — Understand

**Short version of what is expected:**  
Recognize this as dynamic connectivity with only edge additions. Lines are built one at a time, and after each line the candidate must answer whether two substations are in the same grid component. The output is one boolean per operation, in order.

**Related LeetCode problem:**  
LeetCode 684 — Redundant Connection: https://leetcode.com/problems/redundant-connection/  
This is different. It also adds edges one at a time with Union-Find, but it returns the single edge that closes a cycle. It does not answer a connectivity query after every edge, so the output format differs.

**Key constraints:**
- Substations are labeled `0` to `n - 1`
- Each operation is `(substation_origin, substation_destination, grid_query_node_a, grid_query_node_b)`
- The line is built first, then the query is answered
- Lines are never removed and have no weights

---

## Short Interviewer phrases and questions

**Understand**
- “Can you walk me through what the problem is asking?”
- “What does a query return?”
- “Does a query see only the lines built so far?”

**Match**
- “What kind of problem does this remind you of?”
- “Do edges ever get removed?”
- “Do the lines have weights, or only connectivity matters?”

**Plan**
- “Can you describe your approach step by step?”
- “What information do you need to store for each substation?”
- “How will you check whether two substations are in the same component?”

**Implement**
- “Go ahead and code your solution.”
- “Talk me through your implementation as you write it.”
- “What does `find` return, and why?”

**Review**
- “Can you walk through the happy path example with your solution?”
- “What happens if a line connects a substation to itself?”
- “What happens if the same line is built twice?”

**Evaluate**
- “What’s the time complexity per operation?”
- “What’s the space complexity?”
- “What is the worst-case depth of your `find`? Can that cause a problem?”

## Possible candidate answers

### Understand
“We process operations in order. Each operation adds a line, then answers whether the two query substations are connected using only the lines built so far. The output is one boolean per operation.”

### Match
“Lines are only added and we need connectivity at any point, with no weights involved. That is a Disjoint Set Union problem: `union` merges two components, and `find` returns the representative of a substation’s component.”

### Plan
“I’ll make a DSU class where each substation starts as its own parent. For each operation I’ll union the origin and destination, then compare the roots of the two query nodes and append the result. `find` will use path compression so later lookups are faster.”

### Implement
“I’ll store parents in a dict. `find` checks whether the substation is its own parent, and if not, recurses to the root and points the substation straight at it. `union` finds both roots and sets one parent to the other when they differ, returning `True` for a merge and `False` otherwise.”

### Review
“Dry run on the happy path with 6 substations: `(0,1)` merges 0 into 1, and query `(0,2)` is `False` because 2 is alone. `(1,2)` merges 1 into 2, so `find(0)` now resolves to 2 and query `(0,2)` is `True`. Self-loops and duplicate lines make `union` see equal roots and return `False`, so nothing changes.”

### Evaluate
“Each operation is one `union` and two `find` calls. With path compression alone, the amortized cost per operation is `O(log n)`. If I add union by size, it drops to `O(α(n))`, effectively constant. Space is `O(n)` for the parent dict. Result storage is `O(q)` for the output.”

---

## U — Understand

**What the candidate should clarify / restate:**
- Input is `n`, plus a sequence of `(origin, destination, node_a, node_b)` tuples
- Each tuple builds a line first, then queries connectivity
- A query sees every line built up to and including its own operation
- A substation is always connected to itself, so `node_a == node_b` returns `True`
- The output is a list of booleans, one per operation

**Helpful interviewer phrases:**
- “Can you restate the problem in your own words?”
- “Does the query see the line built in the same operation?”
- “If `node_a` and `node_b` are the same substation, what should we return?”
- “What exactly are we returning?”
- “How large can `n` and the number of operations get?”

---

## M — Match

**Technique that fits the problem:**
1. Disjoint Set Union (Union-Find) with path compression

**Why it fits:**
- Edges are added incrementally
- Only component membership is queried, not distances or paths
- Lines have no weights

---

## P — Plan

```python
# DISJOINT SET UNION
# ------------------
# parent[substation] = substation for every substation
# results = []
# for each operation (origin, destination, node_a, node_b):
#   union(origin, destination)
#   append find(node_a) == find(node_b) to results
# return results
#
# find(substation):
#   if parent[substation] is not substation:
#       parent[substation] = find(parent[substation])   # path compression
#   return parent[substation]
#
# union(a, b):
#   root_a = find(a)
#   root_b = find(b)
#   if root_a != root_b:
#       parent[root_a] = root_b
#       return True
#   return False
```

---

## I — Implement

```python
class SubstationDisjointSetUnion:
    def __init__(self, n):
        self.substation_grid_roots = {substation: substation for substation in range(n)}

    def find(self, substation):
        if self.substation_grid_roots[substation] != substation:
            self.substation_grid_roots[substation] = self.find(self.substation_grid_roots[substation])
        return self.substation_grid_roots[substation]

    def union(self, substation_a, substation_b):
        root_a = self.find(substation_a)
        root_b = self.find(substation_b)
        if root_a != root_b:
            self.substation_grid_roots[root_a] = root_b
            return True
        return False

def dsu_smart_grid_connectivity(n, grid_operations):
    substation_dsu = SubstationDisjointSetUnion(n)
    results = []

    for substation_origin, substation_destination, grid_query_node_a, grid_query_node_b in grid_operations:
        substation_dsu.union(substation_origin, substation_destination)
        is_connected = substation_dsu.find(grid_query_node_a) == substation_dsu.find(grid_query_node_b)
        results.append(is_connected)

    return results
```

---

## R — Review

- Walk through the happy path with the operations below. Expected output is `[False, True, False, True, True]`:
  - `(0, 1, 0, 2)` gives `False`
  - `(1, 2, 0, 2)` gives `True`
  - `(3, 4, 3, 5)` gives `False`
  - `(4, 5, 3, 5)` gives `True`
  - `(0, 3, 0, 5)` gives `True`
- Single substation: `n = 1`, operation `(0, 0, 0, 0)` gives `[True]`
- Isolated subnets: with no lines built, a query on two different substations gives `False`, and a query on the same substation gives `True`
- Duplicate line installation: the second `union` sees equal roots and returns `False`, so nothing changes
- Self-loop: `union(x, x)` sees equal roots and changes nothing
- Deep chains: lines `(0,1)`, `(1,2)`, …, `(n-2, n-1)` with no union by size build a parent chain of length `n`. A later `find(0)` then recurses `n` levels deep, which can hit Python’s recursion limit for large `n`. Ask how they would fix it (iterative `find`, or union by size)

---

## E — Evaluate

**Time: O(log n) amortized per operation**  
  Each operation makes one `union` and two `find` calls. With path compression alone, the amortized cost per call is `O(log n)`.  
  Adding union by size or rank improves this to `O(α(n))`, where `α` is the inverse Ackermann function, which is effectively constant.  
  Total for `m` operations is `O(m log n)` as written.

**Space: O(n)**  
  The `substation_grid_roots` dict holds one entry per substation.  
  Recursion in `find` uses up to `O(n)` stack in the worst case.  
  `results` holds one boolean per operation, which is `O(m)` for the output.
