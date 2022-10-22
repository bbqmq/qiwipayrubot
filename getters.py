from peewee import SqliteDatabase, fn
from .models import User, OutputLog, Token
from . import dbHandlers
from datetime import datetime




async def getCountLogs(userId: int):
    count = OutputLog.select().where(OutputLog.userId == userId).count()
    return(count)


async def getSumOutputs(userId: int):
    sum = OutputLog.select(
        fn.SUM(OutputLog.sum)
    ).where(
        OutputLog.userId == userId
    ).scalar()
    if not(sum):
        sum = 0.0
    return(sum)


async def getCountTokens(userId: int):
    count = Token.select().where(Token.userId == userId).count()
    return(count)


async def getUser(userId: int):
    try:
        user = User.get(User.userId == userId)
        user.logsCount = await getCountLogs(userId)
        user.logsSum = round(await getSumOutputs(userId), 2)
        user.tokensCount = await getCountTokens(userId)
        user.daysIn = await dbHandlers.getDaysInBot(user.regTime)
    except User.DoesNotExist:
        user = None
    return(user)


async def getToken(token: str):
    token = Token.get(Token.token == token)
    return(token)


async def getAllTokens():
    tokens = Token.select()
    return(tokens)


async def getTokens(userId: int):
    tokens = Token.select().where(Token.userId == userId)
    return(tokens)


async def getAllUsers():
    users = User.select()
    return(users)


async def getAllOutputs():
    outputs = OutputLog.select()
    return(outputs)


async def getAllBalanceTokens():
    sum = Token.select(
        fn.SUM(Token.lastBalance)
    ).scalar()
    if not(sum):
        sum = 0.0
    return(sum)


async def getAllCommision():
    sum = OutputLog.select(
        fn.SUM(OutputLog.commision)
    ).scalar()
    if not(sum):
        sum = 0.0
    return(sum)


async def getBalanceTokens(userId: int):
    sum = Token.select(
        fn.SUM(Token.lastBalance)
    ).where(Token.userId == userId).scalar()
    if not(sum):
        sum = 0.0
    return(sum)





