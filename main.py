# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from aiogram.utils import executor
from bs4 import BeautifulSoup
from aiogram import types, Dispatcher
from aiogram import Bot
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

db=sqlite3.connect('user_data.db')
c=db.cursor()

try:
    c.execute('''CREATE TABLE data (
        msg_id integer,
        surname text,
        name text,
        surname2 text,
        passport integer
    )''')
except: pass

response_result = "None"

bot = Bot("TOKEN") 
dp = Dispatcher(bot, storage=MemoryStorage())

editt = InlineKeyboardMarkup(row_width=1)\
.add(InlineKeyboardButton(text='🖊 Изменить данные', callback_data='edit'))

class FSMdata(StatesGroup):
    surname = State()
    name = State()
    surname2 = State()
    passport = State()

@dp.message_handler(commands="start")
async def surname_start(message: types.Message):
    await message.answer("Бот пренадзначен для просмотра результатов ОГЭ только для региона 02 (Башкортостан)!!!\nБот является заменой сайту и используется для вашего же удобства!\nВведите /login для авторизации\n/monitor - для однократного вывода результатов\n/spam_monitor - для флуда информацией\n\nСоветуем отключить уведомления от бота т.к. он будет отправлять данные с сайта кадждые примерно 5 секунд.")
    await message.answer("Ну раз ты сюда зашёл могу предложить VPN. Быстро подключается и легко устанавливаетя на любые смартфоны и ПК. 7 дней бесплатный пробный период. Дальше 50 р/месяц. Если заинтересовал пиши @munstr001")
    print(message.from_user.username)
    with open("ids_20.06.2023.txt", "a") as file:
        file.write(str(message.from_user.username) + "\n")


@dp.message_handler(commands="monitor")
async def surname_start(message: types.Message):
    login=c.execute('SELECT msg_id FROM data WHERE msg_id = ?', (message.from_user.id, ))
    if c.fetchone() is None: await message.answer("Сначала пройдите авторизацию /login")
    else:
        db_msg_id=login.fetchone() 
        db_msg_id = int(db_msg_id[-1])
        print(db_msg_id)
        #db_msg_id=db_msg_id[0] 
        if int(message.from_user.id)==db_msg_id:
            surname=c.execute('SELECT surname FROM data WHERE msg_id = ?', (message.from_user.id, ))
            surname = c.fetchall()
            name=c.execute('SELECT name FROM data WHERE msg_id = ?', (message.from_user.id, ))
            name = c.fetchall()
            surname2=c.execute('SELECT surname2 FROM data WHERE msg_id = ?', (message.from_user.id, ))
            surname2 = c.fetchall()
            passport=c.execute('SELECT passport FROM data WHERE msg_id = ?', (message.from_user.id, ))
            passport = c.fetchall()
            surname=surname[-1][-1]
            name=name[-1][-1]
            surname2=surname2[-1][-1]
            passport=passport[-1][-1]
            asyncio.create_task(background_task1(surname, name, surname2, passport, message))
            return
        else: await message.answer("Сначала пройдите авторизацию /login")


@dp.message_handler(commands="spam_monitor")
async def surname_start(message: types.Message):
    login=c.execute('SELECT msg_id FROM data WHERE msg_id = ?', (message.from_user.id, ))
    if c.fetchone() is None: await message.answer("Сначала пройдите авторизацию /login")
    else:
        db_msg_id=login.fetchone() 
        db_msg_id = int(db_msg_id[-1])
        print(db_msg_id)
        #db_msg_id=db_msg_id[0] 
        if int(message.from_user.id)==db_msg_id:
            surname=c.execute('SELECT surname FROM data WHERE msg_id = ?', (message.from_user.id, ))
            surname = c.fetchall()
            name=c.execute('SELECT name FROM data WHERE msg_id = ?', (message.from_user.id, ))
            name = c.fetchall()
            surname2=c.execute('SELECT surname2 FROM data WHERE msg_id = ?', (message.from_user.id, ))
            surname2 = c.fetchall()
            passport=c.execute('SELECT passport FROM data WHERE msg_id = ?', (message.from_user.id, ))
            passport = c.fetchall()
            surname=surname[-1][-1]
            name=name[-1][-1]
            surname2=surname2[-1][-1]
            passport=passport[-1][-1]
            asyncio.create_task(background_task2(surname, name, surname2, passport, message))
            return
        else: await message.answer("Сначала пройдите авторизацию /login")


@dp.message_handler(commands="login", state=None)
async def login(message: types.Message):
    if c.fetchone() is None:
        await message.answer("Сначала пройдите авторизацию /login")
        await message.answer("Введите фамилию: ")
        await FSMdata.surname.set()
    else:    
        await message.answer("Вы уже залогинены. Введите /monitor для однократного вывода информации или /spam_monitor для флуда информацией\n\nЕсли вы хотите изменить данные нажмите кнопку ниже:", reply_markup=editt, parse_mode="HTML")
  
        
        #asyncio.create_task(background_task(message))
        #await message.answer("Hello")

@dp.callback_query_handler(lambda call: True, state=None)
async def edit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data=='edit':
        await state.finish()
        c.execute('DELETE FROM data WHERE msg_id = ?', (callback_query.message.from_user.id, ))
        db.commit()
        await callback_query.message.answer(text='Введите новые данные')
        await callback_query.message.answer("Введите фамилию: ")
        await FSMdata.surname.set()


@dp.message_handler(state=FSMdata.surname)
async def surname_end_and_name_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
        await FSMdata.next()
    await message.answer("Введите имя: ")

@dp.message_handler(state=FSMdata.name)
async def name_end_and_surname2_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMdata.next()
    await message.answer("Введите отчество: ")

@dp.message_handler(state=FSMdata.surname2)
async def surname2_end_and_passport_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname2'] = message.text
        await FSMdata.next()
    await message.answer("Введите номер паспорта: ")

@dp.message_handler(state=FSMdata.passport)
async def passport_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['passport'] = message.text
        msg_id = message.from_user.id
        surname = data["surname"]
        name = data["name"]
        surname2 = data["surname2"]
        passport = data["passport"]
    c.execute('INSERT INTO data VALUES(?, ?, ?, ?, ?)', (msg_id, surname, name, surname2, passport))
    db.commit()
    #asyncio.create_task(background_task1(surname, name, surname2, passport, message))
    #await message.answer("Введите имя: ")
    await message.answer("Авторизация прошла успешно")
    await state.finish()

async def background_task1(surname, name, surname2, passport, message: types.Message):
    #if message.from_user.id == 1983759935:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = Service(), chrome_options=options)
    with open("name_20.06.2023.txt", "a", encoding='utf-8') as file:
        file.write(f"{surname} {name} {surname2} {str(message.from_user.id)}\n")
    
    try:
        driver.get("https://rcoi02.ru/gia9_result/")
    except: pass
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[1]").send_keys(surname)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[2]").send_keys(name)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[3]").send_keys(surname2)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[4]").send_keys(passport)

    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/p[1]/input").click()

    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[5]").click()

        
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/p/span[1]"))
    )

    '''
        try:
            surname_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/span/text()")
        except: await message.answer("Введите достоверные данные!!! /monitor")
        try:
            name_file_text = open("name_19.06.2023.txt", "r", encoding='utf-8')
        except FileNotFoundError:
            f = open('name_19.06.2023.txt', 'tw', encoding='utf-8')
            f.close()
            name_file_text = open("name_19.06.2023.txt", "r", encoding='utf-8')
        if surname_name not in name_file_text:
            with open("name_19.06.2023.txt", "a", encoding='utf-8') as file:
                file.write(str(surname_name) + "\n")
    '''
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]")
    except: await message.answer("Введите достоверные данные! /login")
    main_page = driver.page_source

    soup = BeautifulSoup(main_page, "lxml")
    #global table
    try:
        i = 1
        while True:
            global table, subj_name, mark, balls
            table = soup.find_all("tr")[i]
            subj_name = table.find_all("a")[0].text
            mark = table.find_all("td")[4].text
            balls = table.find_all("td")[3].text
            await message.answer(f"Предмет: {'<code>'}{subj_name}{'</code>'}\nОценка: {'<code>'}{mark}{'</code>'}\nБаллы: {'<code>'}{balls}{'</code>'}", parse_mode="HTML")
                
                #except: await message.answer("Нажмите /start и введите достоверные данные!")
            i += 1
    except IndexError: await message.answer("—————————————")
    await asyncio.sleep(2)


async def background_task2(surname, name, surname2, passport, message: types.Message):
    #if message.from_user.id == 1983759935:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service = Service(), options=options)
    
    while True:
        try:
            driver.get("https://rcoi02.ru/gia9_result/")
        except: pass
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[1]").send_keys(surname)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[2]").send_keys(name)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[3]").send_keys(surname2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[4]").send_keys(passport)

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/p[1]/input").click()

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/form/input[5]").click()

            
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/p/span[1]"))
        )

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]")
        except: await message.answer("Введите достоверные данные! /login")
        main_page = driver.page_source

        main_page = driver.page_source

        soup = BeautifulSoup(main_page, "lxml")
        #global table
        try:
            i = 1
            while True:
                global table, subj_name, mark, balls
                table = soup.find_all("tr")[i]
                subj_name = table.find_all("a")[0].text
                mark = table.find_all("td")[4].text
                balls = table.find_all("td")[3].text
                await message.answer(f"Предмет: {'<code>'}{subj_name}{'</code>'}\nОценка: {'<code>'}{mark}{'</code>'}\nБаллы: {'<code>'}{balls}{'</code>'}", parse_mode="HTML")
                    
                    #except: await message.answer("Нажмите /start и введите достоверные данные!")
                i += 1
        except IndexError:
            await message.answer("—————————————")
        
        #print(response_result)
        await asyncio.sleep(2)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
