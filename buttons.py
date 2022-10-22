from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


async def main():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('✉️ Рассылка', callback_data='admin&mailing'),
        InlineKeyboardButton('📊 Статистика', callback_data='admin&stats'),
        InlineKeyboardButton('💎 Монетизация', callback_data='admin&monetization')
    )
    return(keyboard)


async def backAdmin():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('◀️ Назад', callback_data='admin&menu')
    )
    return(keyboard)


async def downloadTokens():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('⬇️ Загрузить токены', callback_data='admin&download'),
        InlineKeyboardButton('◀️ Назад', callback_data='admin&menu')
    )
    return(keyboard)


async def changeMonetization():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('💳 Реквизиты', callback_data='admin&changeRequisites'),
        InlineKeyboardButton('♻️ Процент', callback_data='admin&changePercent')
    )
    return(keyboard)
