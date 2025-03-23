from dateutil.relativedelta import relativedelta
from datetime import datetime

def declension(number, words):
    if number % 10 == 1 and number % 100 != 11:
        return f"{number} {words[0]}"
    elif 2 <= number % 10 <= 4 and not (12 <= number % 100 <= 14):
        return f"{number} {words[1]}"
    else:
        return f"{number} {words[2]}"

def get_remaining_time(end_time):
    current_date = datetime.now()
    remaining_time = relativedelta(end_time, current_date)
    time_units = [
        (remaining_time.years, ["год", "года", "лет"]),
        (remaining_time.months, ["месяц", "месяца", "месяцев"]),
        (remaining_time.days, ["день", "дня", "дней"]),
        (remaining_time.hours, ["час", "часа", "часов"]),
        (remaining_time.minutes, ["минута", "минуты", "минут"])
    ]
    time_parts = [declension(value, words) for value, words in time_units if value > 0]

    response = "До конца подписки осталось: " + ", ".join(time_parts)
    return response
