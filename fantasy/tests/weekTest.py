import datetime

# def get_dates():
#     today = datetime.date.today()
#     yesterday = datetime.date.today() - datetime.timedelta(days=1)
#     yesterdayString = yesterday.strftime('%b').upper() + ' ' +  str(yesterday.day) + ', ' + str(yesterday.year)
#     todayString = today.strftime('%b').upper() + ' ' +  str(today.day) + ', ' + str(today.year)
#     return(today, yesterday, todayString, yesterdayString)

# today, yesterday, todayString, yesterdayString = get_dates()

today = datetime.datetime.today()
week = []
for i in range(7):
    day = today - datetime.timedelta(i)
    print(day.weekday())
    dayf = day.strftime('%Y-%m-%d')
    week.append(dayf)


# today = datetime.datetime.today().strftime('%Y-%m-%d')
# yesterday = today - datetime.timedelta(1)
print(week)
print(week[0])
print(type([]))