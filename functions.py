def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

def get_days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:  
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    else:
        raise ValueError("Invalid month. Month should be between 1 and 12.")