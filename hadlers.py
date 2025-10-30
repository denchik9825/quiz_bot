from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram import F
from aiosql import update_quiz_index, get_quiz_index,update_quiz_status, get_status, start_new_quiz
from database import quiz_data
from keyboard import generate_opting_keyboard, cmd_start_keyboard, final_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_strat(message: types.Message):
    kb_start = cmd_start_keyboard()
    await message.answer('Добро пожаловать в Квиз', reply_markup=kb_start)


@router.message(F.text=="Начать викторину")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer('Давайте начнем викторину', reply_markup = types.ReplyKeyboardRemove())
    await new_quiz(message)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_status = 0
    await update_quiz_status(user_id, current_status)
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_opting_keyboard(opts,opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id = callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = None
    )
    await callback.message.answer(f"Вы верно ответили")

    current_question_index =  await get_quiz_index(callback.from_user.id)
    current_question_index +=1

    await update_quiz_index(callback.from_user.id, current_question_index)
    current_status_quiz = await get_status(callback.from_user.id)
    current_status_quiz = current_status_quiz + 1
    await update_quiz_status(callback.from_user.id, current_status_quiz)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer('Это был последний вопрос!', reply_markup=final_keyboard())

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id = callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = None
    )
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]["correct_option"]
    await callback.message.answer(f"Вы ответили неправильно\n, правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    current_status_quiz = await get_status(callback.from_user.id)
    current_status_quiz = current_status_quiz + 0
    await update_quiz_status(callback.from_user.id, current_status_quiz)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)

    else:
        await callback.message.answer("Это был последний вопрос", reply_markup=final_keyboard())

@router.message(F.text == "Посмотерть статистику")
async def status_quiz(message: types.Message):
    status_result = await get_status(message.from_user.id)
    if status_result >= 8:
        await message.answer(f"Вы ответили на {status_result} из {len(quiz_data)}\n Выбольшой молодец и хорошо усвоили базовые знания по Python")

    elif status_result < 8 and status_result > 4:
        await message.answer(f"Вы ответили на {status_result} из {len(quiz_data)}.\n Вам стоит подтянуть базовые знания Python")
    else:
        await message.answer(f"Вы ответили на {status_result} из {len(quiz_data)}.\n Вам стоит заново изучить базовые знания Python")
@router.message(F.text =='Сбросить результаты и начать заново quiz')
async def delete_stats_quiz(message: types.Message):
    user_id = message.from_user.id
    await start_new_quiz(user_id)
    await message.answer('Ваши результаты успешно сброшены ')
    await cmd_strat(message)