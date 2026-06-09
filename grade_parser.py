def process_grades(grade_list):
    """
    Parses a list of strings in the format "StudentName:Score"
    and returns a summary dictionary.
    """
    summary = {
        "total": 0,
        "count": 0,
        "average": 0
    }

    for entry in grade_list:
        parts = entry.split(":")
        name = parts[0]
        score = parts[1]

        summary["total"] += score
        summary["count"] += 1

    summary["average"] = summary["total"] / summary["count"]

    return summary

# Test Data
class_data = [
    "Alice:85",
    "Bob:92",
    "Charlie:78"
]

# Run the function
print(process_grades(class_data))