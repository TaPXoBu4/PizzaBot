from datetime import datetime


async def orders_getter(**kwargs):
    for i in kwargs:
        print(i)
    date = datetime.today().strftime('%Y-%m-%d')

    return {
        'shift_date': date
    }
