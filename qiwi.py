from loader import db
import aiohttp
import asyncio
import json

loop = asyncio.get_event_loop()

class Api:
    def __init__(self):
        self.profileUrl = 'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=false&contractInfoEnabled=true&userInfoEnabled=false'
        self.balanceUrl = 'https://edge.qiwi.com/funding-sources/v2/persons/{number}/accounts'
        self.sendPayment = 'https://edge.qiwi.com/sinap/api/v2/terms/{id}/payments'

    async def setToken(self, token: str):
        self.headers = {
            'Accept': 'application/json',
            'authorization': f'Bearer {token}',
            'User-Agent': 'Android v3.2.0 MKT'
        }

    async def getNumberQiwi(self):
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.profileUrl, headers=self.headers) as response:
                if response.status != 200:
                    return(None)
                responseJson = await response.json()
                return(responseJson['contractInfo']['contractId'])

    async def getBlockInfo(self):
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.profileUrl, headers=self.headers) as response:
                if response.status != 200:
                    return(401)
                responseJson = await response.json()
                return(responseJson['contractInfo']['blocked'])

    async def getBalance(self, number):
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.balanceUrl.format(number=number), headers=self.headers) as response:
                if response.status != 200:
                    return(response.status)
                responseJson = await response.json()
                return(responseJson['accounts'][0]['balance']['amount'])

    async def sendMoney(self, data, id):
        async with aiohttp.ClientSession() as client:
            async with client.post(url=self.sendPayment.format(id=id), json=data, headers=self.headers) as response:
                if response.status != 200:
                    return(None)
                responseJson = await response.json()
                return(responseJson)

async def uploadTokens(userId: int, tokenList: list):
    qiwi = Api()
    success, denied, generalBalance = 0, 0, 0
    for token in tokenList:
        await loop.create_task(qiwi.setToken(token))
        number = await loop.create_task(qiwi.getNumberQiwi())
        if not(number):
            denied += 1
            continue
        success += 1
        balance = await loop.create_task(qiwi.getBalance(number))
        generalBalance += balance
        await loop.create_task(db.newToken(userId, number, token, balance))
    return([success, denied, generalBalance])
