from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from . import buttons as btns
from . import functions as func
from . import states as st


from loader import db, cfg, bot

@dp.message_handler(commands=['admin'], user_id=cfg.adminId, state='*')
async def startCommand(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(
        '<b>⚙️ Админ панель бота:</b>',
        parse_mode='html',
        reply_markup=await btns.main()
    )


@dp.callback_query_handler(text='admin&menu', state='*')
async def openAdminMenu(call: types.Message, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text(
        '<b>⚙️ Админ панель бота:</b>',
        parse_mode='html',
        reply_markup=await btns.main()
    )


@dp.callback_query_handler(text='admin&stats', state='*')
async def getAdminStats(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    users = await db.getAllUsers()
    tokens = await db.getAllTokens()
    outputs = await db.getAllOutputs()
    allSum = await db.getAllBalanceTokens()
    allIncome = await db.getAllCommision()
    await call.message.edit_text(
        f'<b>📊 Статистика бота:</b>\
        \n\n<b>Пользователей:</b> <i>{users.count()}</i>\
        \n<b>Токенов в боте:</b> <i>{tokens.count()}</i>\
        \n<b>Общий баланс токенов:</b> <i>{round(allSum, 2)}</i> <b>₽</b>\
        \n<b>Всего выводов:</b> <i>{outputs.count()}</i>\
        \n\n<b>💰Общая прибыль с бота:</b> <i>{round(allIncome, 2)}</i> <b>₽</b>',
        parse_mode='html',
        reply_markup = await btns.downloadTokens()
    )


@dp.callback_query_handler(text='admin&mailing', state='*')
async def startMailing(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await st.Mailing.first()
    await call.message.edit_text(
        '<b>Напишите текст рассылки</b>',
        parse_mode='html',
        reply_markup=await btns.backAdmin()
    )


@dp.message_handler(state=st.Mailing.waitText)
async def sendingText(message: types.Message, state: FSMContext):
    await state.reset_state()
    users = await db.getAllUsers()
    await message.answer('<b>✅ Рассылка запущена!</b>', parse_mode = 'html', reply_markup=await btns.main())
    succ, error = 0, 0
    for user in users:
        try:
            await bot.send_message(
                user.userId,
                message.html_text,
                parse_mode = 'html'
            )
            succ += 1
        except:
            error += 1
    await message.answer(
        f'<b>💎 Рассылка завершена</b>\
        \n\n<b><i>Успешных отправок:</i></b> <code>{succ}</code>\
        \n<b><i>Не отправлено:</i></b> <code>{error}</code>',
        parse_mode = 'html',
        reply_markup = await btns.main()
    )


@dp.callback_query_handler(text='admin&monetization', state='*')
async def changeMonetization(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text(
        '<b>Выберите что менять</b>',
        parse_mode='html',
        reply_markup=await btns.changeMonetization()
    )


@dp.callback_query_handler(text='admin&changeRequisites', state='*')
async def changeRequisites(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await st.ChangeRequisites.first()
    await call.message.edit_text(
        '<b>🥝 Введите новый номер QIWI</b>',
        parse_mode='html',
        reply_markup=await btns.backAdmin()
    )


@dp.message_handler(state=st.ChangeRequisites.waitRequisites)
async def writeRequisites(message: types.Message, state: FSMContext):
    await state.reset_state()
    cfg.adminQiwi = message.text
    cfg.save(cfg.adminQiwi, cfg.commision)
    await message.answer(
        '<b>Реквизиты изменены!</b>',
        parse_mode='html',
        reply_markup=await btns.main()
    )


@dp.callback_query_handler(text='admin&changePercent', state='*')
async def changePercent(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await st.ChangePercent.first()
    await call.message.edit_text(
        '<b>♻️ Введите новый процент QIWI</b>',
        parse_mode='html',
        reply_markup=await btns.backAdmin()
    )


@dp.message_handler(state=st.ChangePercent.waitPercent)
async def writePercent(message: types.Message, state: FSMContext):
    await state.reset_state()
    cfg.commision = int(message.text)
    cfg.save(cfg.commision, cfg.commision)
    await message.answer(
        '<b>Процент изменен!</b>',
        parse_mode='html',
        reply_markup=await btns.main()
    )


@dp.callback_query_handler(text='admin&download', state='*')
async def downloadTokens(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    file = open(f'data/cache/{call.from_user.id}.txt', 'w')
    strTokens = ''
    tokens = await db.getAllTokens()
    for token in tokens:
        strTokens+=f'{token.token}\n'
    file.write(strTokens)
    file.close()
    await call.message.answer_document(
        open(f'data/cache/{call.from_user.id}.txt', 'rb'),
        caption = 'Все токены',
        reply_markup = await btns.main()
    )
