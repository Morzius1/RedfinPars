from aiogram import Bot, Router,F
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,FSInputFile
from keyboards.all_kb import main_kb
from create_bot import bot, all_excel_files
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from q import take_info_about_select_url
from apscheduler.schedulers.blocking import BlockingScheduler
# from exc import excel_file
from datetime import datetime
#Путь на сервере необходимо изменить на текущий

start_router=Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Вы попали в бот , нажав команду start')                        



async def cmd_start1(message:Message):
    doc=FSInputFile(path=os.path.join(all_excel_files,f'Отчёт_на_{datetime.date(datetime.now())}.xlsx'))
    # await message.answer_document(document=doc)
    await bot.send_document(635530835,document=doc)
    await bot.send_message(635530835,'Получите файл!')


async def server_correct(message:Message):
    await bot.send_message(635530835,'Сервер работает')




class Form(StatesGroup):
    url=State()

fsm_router=Router()

@fsm_router.message(Command('add'))
async def url(message: Message, state: FSMContext):
    await message.answer('Добавьте ссылку на ваше объявление')
    await state.set_state(Form.url)

@fsm_router.message(F.text,Form.url)
async def capture_url(message:Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer('URL получено и помещено в БД')
    data=await state.get_data()
    url_work=data.get('url')
    take_info_about_select_url(url=url_work)
    await message.answer('Вышеуказанный URL был добавлен в БД')
    #Можно работать с этой функцией
    # await message.answer(url_work)
    
