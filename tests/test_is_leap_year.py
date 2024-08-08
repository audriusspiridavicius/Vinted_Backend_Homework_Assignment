from functions import is_leap_year
import pytest



class TestIsLeapYear:
    @pytest.mark.parametrize("year", [1900, 1921, 1970, 1981, 2001, 2021, 2022, 2023, 2025, 2026, 2997])
    def test_year_is_not_leap(self, year):
        
        assert is_leap_year(year) == False
        
    @pytest.mark.parametrize("year", [1972, 1980, 2000, 2020, 2024, 2028, 2032, 2036, 2996])
    def test_year_is_leap(self, year):
        
        assert is_leap_year(year) == True