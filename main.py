from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from base import create_table

from aiogram import executor
from aiogram.types import *
from model import Task_list

TOKEN = '6333919153:AAHzjso9BpSibl0RB6Gd-1gZd3lgkC3H1sA'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start", "help"])
async def start(message: Message ):
    await message.answer ("Привет! Ты можешь создать лист задач. Вот мои команды:\n" \
                 "/add <задача> - добавь новую задачу 📝\n" \
                 "/done <индекс> - если ты сделал задачу 👌\n" \
                 "/list - все списки задач 📋\n" \
                 "/delete <индекс> - удалить задачу 🚽\n")
    

@dp.message_handler(commands=["add"])
async def add(message: Message):
    task_text = message.text[5:].strip() # Получаем текст задачи после команды "/add "
    if not task_text:   
        await message.reply('Укажите текст задачи')
        return
    
    task = Task_list(task_text, "невыполнена")
    task.save()
    await message.reply("Задача успешно добавлена!")

@dp.message_handler(commands=["done"])
async def done(message: Message):
    task_id = int(message.text[6:])  # Получаем индекс задачи после команды "/done "
    tasks = Task_list.get_all()

    if task_id < 1 or task_id > len(tasks) :
        await message.reply("Добавьте номер задачи !")
        return

    task = tasks[task_id - 1]
    Task_list.mark_as_done(task_id)
    await message.reply(f"Задача '{task.title}' сделанно !")

@dp.message_handler(commands=["list"])
async def list(message: Message):
    tasks = Task_list.get_all()
    if not tasks:
        await message.reply("Список задач пуст!")
        return
    reply_text = "Список задач:\n"
    for i, task in enumerate(tasks):
        status = "🟩" if task.status == "выполнена" else "🟥"
        reply_text += f"{i + 1}. {status} {task.title}\n"

    await message.reply(reply_text)

@dp.message_handler(commands=["delete"])
async def delete(message: Message):
    task_id = int(message.text[8:])  # Получаем  задачи после команды "/delete "
    tasks = Task_list.get_all()

    if task_id < 1 or task_id > len(tasks):
        await message.reply("Некоректный индекс в списке задач!")
        return

    task = tasks[task_id - 1]
    Task_list.delete(task_id)
    await message.reply(f"Задача '{task.title}' удалена!")

@dp.message_handler()
async def unknown(message: Message):
    await message.reply("Неизвестная команда. Введите /help для получения списка команд.")

if __name__ == '__main__':
    
    create_table()
    executor.start_polling(dp, skip_updates=True)