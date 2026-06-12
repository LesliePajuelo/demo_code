import pytest
from grade_parser import process_grades


@pytest.fixture
def large_dataset():
    """Generate 100+ entries for stress testing."""
    return [f"Student{i}:{50 + (i % 51)}" for i in range(150)]


class TestProcessGrades:
    def test_empty_array(self):
        """Empty list should raise ZeroDivisionError on average calc."""
        with pytest.raises(ZeroDivisionError):
            process_grades([])

    def test_negative_scores(self):
        """Handle negative scores."""
        result = process_grades(["Alice:-10", "Bob:-5"])
        assert result["total"] == -15
        assert result["count"] == 2
        assert result["average"] == -7.5

    def test_zero_score(self):
        """Handle zero scores."""
        result = process_grades(["Alice:0", "Bob:100"])
        assert result["total"] == 100
        assert result["count"] == 2
        assert result["average"] == 50

    def test_large_dataset(self, large_dataset):
        """Process 100+ entries."""
        result = process_grades(large_dataset)
        assert result["count"] == 150
        assert result["total"] > 0
        assert result["average"] > 0

    def test_complex_number_string(self):
        """Complex numbers as strings should fail on int() conversion."""
        with pytest.raises(ValueError):
            process_grades(["Alice:3+4j"])

    def test_swapped_key_values(self):
        """Swapped format (score:name) fails on int() conversion."""
        with pytest.raises(ValueError):
            process_grades(["85:Alice", "92:Bob"])

    def test_normal_case(self):
        """Standard case with valid data."""
        result = process_grades(["Alice:85", "Bob:92", "Charlie:78"])
        assert result["total"] == 255
        assert result["count"] == 3
        assert result["average"] == 85
