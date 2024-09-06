import asyncio
from create_bot import bot,dp
from handlers.start import start_router, fsm_router,cmd_start1
from aiogram.types import Message,BotCommandScopeDefault,BotCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from q import take_url_in_db,take_info_about_flats
from exc import excel_file
from db import create_table, select_from_info_flats
from datetime import datetime

async def set_commands():
    commands = [BotCommand(command='add', description='Добавить ссылку на объект'),
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая выполнится когда бот запустится
async def start_bot():
    await set_commands()



async def main():
    # регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(fsm_router)
    #Cоздание задач по определенному таймингу
    sh=BlockingScheduler()
    sh = AsyncIOScheduler(timezone='Europe/Moscow')
    # Запуск задачи №1 - собираем URL в БД
    sh.add_job(take_url_in_db,'cron',day_of_week='mon-sun',hour=23,minute=45,misfire_grace_time=60 * 5,max_instances=1)
    # Запуск задачи №2 - собираем информацию о квартирах в БД
    sh.add_job(take_info_about_flats,'cron',day_of_week='mon-sun',hour=23,minute=52,misfire_grace_time=60 * 5,max_instances=1)
    # Запуск задачи №3 - формируем excel файл 
    sh.add_job(excel_file,'cron',day_of_week='mon-sun',hour=23,minute=55,
               kwargs={'dict_list':select_from_info_flats(), 'output_filename':f'Отчёт_на_{datetime.date(datetime.now())}.xlsx'},misfire_grace_time=60 * 5,max_instances=1)
    # #Запуск задачи №4 - отправка отчёта
    sh.add_job(cmd_start1,'cron',day_of_week='mon-sun',hour=23,minute=56,kwargs={'message':  Message},misfire_grace_time=60 * 5,max_instances=1)
    sh.start()
    dp.startup.register(start_bot)
    
    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
      await bot.delete_webhook(drop_pending_updates=True)
      await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
      await bot.session.close()

if __name__=='__main__':
    asyncio.run(main())