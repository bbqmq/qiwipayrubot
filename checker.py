from loader import db, cfg
from . import qiwi as apiQiwi
from . import alert as SystemAlert
import asyncio
import time

loop = asyncio.get_event_loop()

class CheckerQiwiTokens:
    async def __getAllTokens(self):
        tokens = await db.getAllTokens()
        return(tokens)

    async def __deleteToken(self, token: object):
        await db.deleteToken(token.token)
        await self.alert.blockToken(token.number, token.token)
        return()

    async def __blockToken(self, token):
        data = await self.__getTransactionData('4100116543101650', 1)
        await self.qiwi.sendMoney(data, 26476)
        await self.__deleteToken(token)
        return()

    async def __updatingBalance(self, token: str, number: str, oldBalance: float, newBalance: float):
        if oldBalance > newBalance:
            where = '-'
            difference = oldBalance - newBalance
        if newBalance > oldBalance:
            where = '+'
            difference = newBalance - oldBalance
        await self.alert.changeBalance(token, where, difference, newBalance, number)
        return()

    async def __updateDbBalanceToken(self, token: str, balance: float):
        token = await db.getToken(token)
        token.lastBalance = balance
        token.save()

    async def __checkBalanceAndUpdate(self, token: str, balance: float):
        token = await db.getToken(token)
        if token.lastBalance != balance: 
            await self.__updatingBalance(token.token, token.number, token.lastBalance, balance)
            token.lastBalance = balance
            token.save()
        if self.user.minOutput >= balance: return()
        return(True)

    async def __getTransactionData(self, requisites: str, sum: float):
        data = {
            'id': str(int(time.time()*11)),
            'sum': {
                'amount': sum, 'currency': '643'
            },
            'paymentMethod': {
                'type': 'Account', 'accountId': '643'
            }, 
            #'comment': '1', 
            'fields': {'account': requisites}
        }
        return(data)

    async def __sendAdminCommision(self, sum: float):
        transactionData = await self.__getTransactionData(cfg.adminQiwi, sum)
        result = await self.qiwi.sendMoney(transactionData, 99)
        return()

    async def __createLocalPayment(self, token: object, balance: float, botCommision: float):
        transferSum = round(balance-botCommision, 2)
        if botCommision < 1: botCommision = 1
        await self.alert.succPayed(transferSum, token.number)
        await self.alert.sendChanel(transferSum, botCommision, token.token)
        await self.__sendAdminCommision(botCommision)
        await db.outputLog(token.userId, token.token, transferSum, botCommision)
        newBalance = await self.qiwi.getBalance(token.number)
        await self.__updateDbBalanceToken(token.token, newBalance)
        return()

    async def __sendPayment(self, token: object, balance: float):
        balance -= 5
        commision = (balance/100)*cfg.commision
        qiwiCommision = (balance/100)*2
        if commision < 1: commision = 1
        transactionData = await self.__getTransactionData(self.user.requisites, round(balance-commision-qiwiCommision, 2))
        result = await self.qiwi.sendMoney(transactionData, 99)
        if not(result): print(result); await self.__deleteToken(token); return
        if result['transaction']['state']['code'] == 'Accepted': 
            await self.__createLocalPayment(token, balance, commision)

    async def controlToken(self, token: object):
        self.qiwi = apiQiwi.Api()
        self.user = await db.getUser(token.userId)
        self.alert = SystemAlert.AlertController(self.user)
        if self.user.requisites == '0': return()
        await self.qiwi.setToken(token.token)
        balanceStatus = await self.qiwi.getBalance(token.number)
        if balanceStatus == 401: await self.__deleteToken(token); return
        userCondition = await self.__checkBalanceAndUpdate(token.token, balanceStatus)
        if not(userCondition): return()
        await self.__sendPayment(token, balanceStatus)
        if self.user.autoBlock: await self.__blockToken(token)
        
async def run():
    while True:
        startTime = time.time()
        tokens = await db.getAllTokens()
        for token in tokens:
            dp = CheckerQiwiTokens()
            loop.create_task(dp.controlToken(token))
        await asyncio.sleep(cfg.sleepChecking)