import sqlite3
import pandas as pd
from dotenv import load_dotenv
import os


# Разметка для полей БД
trans_wag = {'id': 'id', 'wagon_number': 'Номер вагона', 'wagon_type': 'Род вагона', 'wagon_subtype': 'Подрод вагона', 'wagon_model': 'Модель вагона', 'construction_date': 'Дата постройки', 'wagon_end_date': 'Срок службы', 'wagon_supplier': 'Поставщик', 'client': 'Клиент', 'business_activity_typ': 'Вид деятельности'}
trans_prof = {'id': 'id','date': 'Дата', 'profitability_plan': 'Плановая<br>доходность', 'fleet': 'Парк', 'loading_plan_execution': 'Выполнение<br>плана погрузки', 'average_rate _loaded': 'Средняя ставка<br>на 1 груж в/о', 'empty_shipments': 'Порожние<br>ваг/отпр', 'average_rate_empty': 'Средняя ставка<br>на 1 пор в/о', 'profitability_fact':'Фактическая<br>доходность'}


# Внесение информации о пользователе в БД
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, email: str):
	load_dotenv('.env')
	bd = os.getenv("BD")
	connection = sqlite3.connect(bd, check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, email) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, email))
	connection.commit()
	connection.close()


# Проверка регестрации пользователя в БД
def find_user_id(user_id):
	load_dotenv('.env')
	bd = os.getenv("BD")
	connection = sqlite3.connect(bd)
	cursor = connection.cursor()
	cursor.execute('SELECT user_id FROM users WHERE user_id =:user_id_search', {'user_id_search': user_id})
	results = cursor.fetchall()
	connection.close()
	if len(results) > 0:
		return results[0][0]
	else:
		return 0


# Поиск информации о вагоне в БД
def find_wagon(number):
	global trans_wag
	load_dotenv('.env')
	bd = os.getenv("BD")
	connection = sqlite3.connect(bd)
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM wagons WHERE wagon_number =:number', {'number': number})
	results = list(*cursor.fetchall())
	connection.close()
	connection = sqlite3.connect(bd)
	connection.row_factory = sqlite3.Row
	cursor = connection.execute('select * from wagons')
	row = cursor.fetchone()
	connection.close()
	if len(results) > 0:
		names = row.keys()
		dictionary = dict(zip(names, results))
		info = {}
		for key in dictionary:
			info[trans_wag[key]] = dictionary[key]
		return info
	else:
		return 0


# Информация о доходности из БД для построения диаграммы
def profitability_info(date):
	global trans_prof
	load_dotenv('.env')
	bd = os.getenv("BD")
	connection = sqlite3.connect(bd)
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM profitability WHERE date =:today', {'today': date})
	results = list(*cursor.fetchall())
	connection.close()
	connection = sqlite3.connect(bd)
	connection.row_factory = sqlite3.Row
	cursor = connection.execute('select * from profitability')
	row = cursor.fetchone()
	connection.close()
	if len(results) > 0:
		names = row.keys()
		dictionary = dict(zip(names, results))
		info = {}
		for key in dictionary:
			info[trans_prof[key]] = dictionary[key]
		return info
	else:
		return 0


# Получение из БД адреса электронной почты пользователя
def get_user_email(user_id):
	load_dotenv('.env')
	bd = os.getenv("BD")
	connection = sqlite3.connect(bd)
	cursor = connection.cursor()
	cursor.execute('SELECT email FROM users WHERE user_id =:user_id_search', {'user_id_search': user_id})
	results = cursor.fetchall()
	connection.close()
	if len(results) > 0:
		return results[0][0]
	else:
		return 0


#  Получение из БД информации о вагонах по родам подвижного состава и количества для построения диаграммы
def get_wagon_info():
	load_dotenv('.env')
	bd = os.getenv("BD")
	cnx = sqlite3.connect(bd)
	df = pd.read_sql_query("SELECT wagon_type, wagon_number FROM wagons", cnx)
	df_drp = pd.pivot_table(df,
							index=["wagon_type"],
							values=["wagon_number"],
							aggfunc=[len])
	df_drp = df_drp.reset_index()
	df_drp.columns = ['РПС', 'Количество']
	df_drp['Количество'] = round(df_drp['Количество'] / 1000, 2)
	return df_drp

