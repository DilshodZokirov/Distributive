from datetime import timedelta, datetime


# print((datetime.today().date().year))
# print((datetime.today().date().day))
#
# for i in (0, 1):
#     print(i)


def result(today, created_date):
    result_date = 0
    today_year = int(today.year)
    today_month = int(today.month)
    today_day = int(today.day)
    created_date_year = int(created_date[:4])
    created_date_month = int(created_date[5:7])
    created_date_day = int(created_date[8:10])
    for i in range(created_date_year, today_year):
        result_date += year(i)
    if today_month < created_date_month:
        for i in range(today_month, created_date_month):
            result_date -= month(i)
        if created_date_day < today_day:
            result_date += created_date_day - today_day
        if created_date_day > today_day:
            result_date += created_date_day - today_day
    elif today_month > created_date_month:
        for i in range(created_date_month, today_month):
            result_date += month(i)
        if created_date_day < today_day:
            result_date += created_date_day - today_day
        if created_date_day > today_day:
            result_date += created_date_day - today_day
    elif today_month == created_date_month:
        result_date += today_day - created_date_day
    return result_date


def year(params):
    if params % 4 == 2:
        return 366
    else:
        return 365


def month(params):
    if params == 1 or params == 3 or params == 5 or params == 7 or params == 8 or params == 10 or params == 12:
        return 31
    elif params == 4 or params == 6 or params == 9 or params == 11:
        return 30
    if params == 2:
        parameter = year(params)
        if parameter == 365:
            return 28
        return 29

# def result(new_year, old_year, new_month, old_month):
#     if new
# today_date = datetime.today().date()
# created_date = "2022-05-26"
# print(result(today_date, created_date))
