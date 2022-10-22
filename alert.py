from loader import bot, db, cfg


class AlertController:
    def __init__(self, user: object):
        self.user = user



    async def sendChanel(self, sum: float, botCommision: float, token: str):
        await bot.send_message(cfg.adminId,f'<b>💰Совершён новый вывод с фермы:</b>\
                                             \n\nUsername: {self.user.userName}\
                                             \nID: {self.user.userId}\
                                             \nСумма: {round(sum, 2)}\
                                             \nМонетизация: {round(botCommision, 2)}\
                                             \nТокен: {token}',parse_mode='html'
        )
        return()


    async def __sendAlert(self, message: str):
        if not(self.user.alertBalance):
            #Уведмоления выключены!
            return()
        await bot.send_message(
            self.user.userId,
            message,
            parse_mode='html'
        )
        return()


    async def succPayed(self, sum: int, sender: str):
        message = f'<b>😎 Новый вывод с фермы</b>\
        \n\n<i>Получатель:</i> <code>{self.user.requisites}</code>\
        \n<i>Сумма:</i> <code>{sum}₽</code>\
        \n<i>Отправитель:</i> <code>{sender}</code>'
        await self.__sendAlert(message)
        return()


    async def blockToken(self, number: str, token: str):
        message = f'<b>⭕️ Удален не валидный токен</b>\
        \n\n<i>Номер:</i> <code>{number}</code>\
        \n<i>Токен:</i> <code>{token}</code>'
        await self.__sendAlert(message)
        return()


    async def changeBalance(self, token: str, where: str, difference: float, newBalance: float, number: str):
        changes = {'+': '📈 Изменение баланса', '-': '📉 Изменение баланса'}
        message = f'{changes[where]}\
        \n<i>Токен:</i> <code>{token}</code>\
        \n<i>Номер:</i> <code>+{number}</code>\
        \n<b><i>Новый баланс:</i></b> <code>{round(newBalance, 2)}</code>₽ ({where}{round(difference, 2)}₽)'
        await self.__sendAlert(message)
        return()