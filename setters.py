from peewee import SqliteDatabase, fn
from .models import User, OutputLog, Token
from datetime import datetime



async def newUser(userId: int, firstName: str, userName: str):
    if not(firstName): firstName = 'None'
    if not(userName): userName = 'None'
    User.create(
        userId = userId,
        firstName = firstName,
        userName = userName,
        balance = 0,
        requisites = '0',
        minOutput = 10,
        autoBlock = 0,
        alertBalance = 0,
        regTime = datetime.now().strftime('%d-%m-%Y')
    )
    return()


async def newToken(userId: int, number: str, token: str, lastBalance: float):
    try:
        Token.create(
            userId = userId,
            number = number,
            token = token,
            lastBalance = lastBalance
        )
        return()
    except:
        return()


async def updateAutoBlock(userId: int, status: int):
    user = User.get(User.userId == userId)
    user.autoBlock = status
    user.save()
    return()


async def updateAlertBalance(userId: int, status: int):
    user = User.get(User.userId == userId)
    user.alertBalance = status
    user.save()
    return()


async def updateMinOutput(userId: int, sum: float):
    user = User.get(User.userId == userId)
    user.minOutput = sum
    user.save()
    return()


async def updateRequisites(userId: int, requisites: str):
    user = User.get(User.userId == userId)
    user.requisites = requisites
    user.save()
    return()


async def outputLog(userId: int, token: str, sum: float, commision: float):
    OutputLog.create(
        userId = userId,
        token = token,
        sum = sum,
        commision = commision
    )


async def deleteToken(token: str):
    Token.delete().where(Token.token == token).execute()
    return()


async def clearUser(userId: int):
    try:
        user = User.get(User.userId == userId)
        user.requisites = '0'
        user.minOutput = 10
        user.autoBlock = 0
        user.alertBalance = 0
        user.save()
        tokens = Token.get(Token.userId == userId)
        tokens.delete_instance()
        OutputLog.delete().where(OutputLog.userId == userId)
        return()
    except:
        return()
