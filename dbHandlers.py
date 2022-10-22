import datetime





async def getDaysInBot(date):
    dateList = date.split('-')
    strNowDate = datetime.datetime.now().strftime('%d-%m-%Y-').split('-')

    #2 - Год, 1 - Месяц, 0 - день
    startDate = datetime.datetime(day=int(dateList[0]), month=int(dateList[1]), year=int(dateList[2]))
    nowDate = datetime.datetime(day=int(strNowDate[0]), month=int(strNowDate[1]), year=int(strNowDate[2]))
    differenceDate = nowDate - startDate
    return(differenceDate.days)


