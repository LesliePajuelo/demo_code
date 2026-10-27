# UMPIRE Interview Guide — The Study Break Optimizer

## U — Understand

**Short version of what is expected:**  
Recognize this as an interval scheduling / overlap-removal problem. 
The goal is **not** to return the sessions to keep, but the **minimum number to skip** so the remaining sessions do not overlap.

**Equivalent LeetCode problem:**  
LeetCode 435 — Non-overlapping Intervals: https://leetcode.com/problems/non-overlapping-intervals/

---

## Short Interviewer phrases and questions

**Understand**
- “Can you walk me through what the problem is asking?”
- “What does overlapping mean in this context?”
- “What should the output represent?”

**Match**
- “What kind of problem does this remind you of?”
- “Have you seen anything similar before?”
- “What approaches are you considering?”

**Plan**
- “Can you describe your approach step by step?”
- “What information will you track as you go?”
- “How will you handle overlapping intervals?”

**Implement**
- “Go ahead and code your solution.”
- “Talk me through your implementation as you write it.”
- “What does this part of your code do?”

**Review**
- “Can you walk through an example with your solution?”
- “Does your solution handle edge cases?”
- “Anything you want to double-check?”

**Evaluate**
- “What’s the time complexity?”
- “What’s the space complexity?”

## Possible candidate answers

### Understand
“This is asking for the minimum number of intervals to remove so the rest do not overlap. Touching endpoints are allowed.”

### Match
“This is an intervals greedy problem, similar to Non-overlapping Intervals.”

### Plan
“I’ll sort by end time, keep the earliest-finishing intervals, and count overlaps as removals.”

### Implement
“I’ll use `sorted(..., key=lambda x: x[1])`, track the end of the last kept interval, and increment removals whenever the current interval overlaps.”

### Review
“I’ll dry run a sample and confirm that `[1,2]` and `[2,3]` are allowed, so the condition is `start >= prev_end`.”

### Evaluate
“Time is `O(n log n)`, space is `O(n)` here because I’m using `sorted` to avoid modifying the input.”

---

## U — Understand

**What the candidate should clarify / restate:**
- Input is a list of intervals `[start, end]`
- Two sessions that touch, like `[1,2]` and `[2,3]`, are **not overlapping**
- Need the **minimum removals**
- Constraints are large, so likely better than `O(n^2)`

**Helpful interviewer phrases:**
- “Can you restate the problem in your own words?”
- “What does overlap mean here?”
- “Are intervals that touch considered overlapping?”
- “What exactly are we returning?”
- “Given `n` up to `10^5`, what time complexity should we aim for?”

---

## M — Match

**Algorithmic techniques that could solve the problem:**
1. Greedy by end time  
2. Greedy by start time while keeping smaller end  
3. Dynamic programming  
4. Brute force  

---

## P — Plan

```python
# GREEDY
# ------
# Order inputs by end time
# define removed = 0
# define prev_end as the end of the first interval
# for each remaining interval:
#   if start < prev_end:
#       removed += 1
#   else:
#       take it
#       update prev_end = end
# return removed
```

---

## I — Implement

```python
def eraseOverlapIntervals(sessions):
    if not sessions:
        return 0

    ordered = sorted(sessions, key=lambda interval: interval[1])

    removed = 0
    prev_end = ordered[0][1]

    for start, end in ordered[1:]:
        if start < prev_end:
            removed += 1
        else:
            prev_end = end

    return removed
```

---

## R — Review

- Walk through an example  
- Check duplicates  
- Check touching intervals  
- Check all overlapping  

---
## E — Evaluate
**Time: O(n log n)**
  The dominant operation is sorting the intervals, which takes O(n log n). Python uses TimSort which is O(n log n), 
  if you don't know what the 'under the hood' sorting algo is being used O(n log n) is a reasonable abstraction.
  The subsequent loop that scans through the intervals is O(n).
  Since O(n log n) + O(n) simplifies to O(n log n), sorting dominates.
**Space: O(n)**
  Using sorted(...) creates a new list of size n, so that is O(n) extra space.
  Aside from that, only a few variables are used (removed, prev_end), which is O(1).
  Therefore, total auxiliary space is O(n) due to the copied list.

