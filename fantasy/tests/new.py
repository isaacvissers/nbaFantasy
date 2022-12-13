import datetime

date = datetime.date.today()
monshort = date.strftime('%b')
print(date)
# print(monshort + date.day + ', ' + date.year)
print(date.day)
print(date.string())