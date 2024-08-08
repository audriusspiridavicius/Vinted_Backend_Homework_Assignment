from functions import get_days_in_month
import pytest

class TestGetDaysInMonth:
    
    @pytest.mark.parametrize("year, month, expected_days_value", [(1999, 2, 28), (2000, 2, 29),
                                                                  (2000, 3, 31), (2000, 4, 30),
                                                                  (2001, 4, 30), (2024, 12, 31)])
    def test_correct_days_number_returned(self,year, month, expected_days_value):
        
        assert get_days_in_month(year, month) == expected_days_value