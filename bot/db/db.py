import sqlite3
import pandas
import datetime
from bot.other_methods.dash_board import paint_waterfall_chart

# current_date = datetime.datetime.now().strftime('%d.%m.%Y')
# print(current_date)


trans_wag = {'id': 'id', 'wagon_number': 'Номер вагона', 'wagon_type': 'Род вагона', 'wagon_subtype': 'Подрод вагона', 'wagon_model': 'Модель вагона', 'construction_date': 'Дата постройки', 'wagon_end_date': 'Срок службы', 'wagon_supplier': 'Поставщик', 'client': 'Клиент', 'business_activity_typ': 'Вид деятельности'}
trans_prof = {'id': 'id','date': 'Дата', 'profitability_plan': 'Плановая<br>доходность', 'fleet': 'Парк', 'loading_plan_execution': 'Выполнение<br>плана погрузки', 'average_rate _loaded': 'Средняя ставка<br>на 1 груж в/о', 'empty_shipments': 'Порожние<br>ваг/отпр', 'average_rate_empty': 'Средняя ставка<br>на 1 пор в/о', 'profitability_fact':'Фактическая<br>доходность'}

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, email: str):
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database', check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, email) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, email))
	connection.commit()
	connection.close()


def find_user_id(user_id):
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	cursor = connection.cursor()
	cursor.execute('SELECT user_id FROM users WHERE user_id =:user_id_search', {'user_id_search': user_id})
	results = cursor.fetchall()
	connection.close()
	if len(results) > 0:
		return results[0][0]
	else:
		return 0


def find_wagon(number):
	global trans_wag
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM wagons WHERE wagon_number =:number', {'number': number})
	results = list(*cursor.fetchall())
	connection.close()
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	connection.row_factory = sqlite3.Row
	cursor = connection.execute('select * from wagons')
	row = cursor.fetchone()
	names = row.keys()
	dictionary = dict(zip(names, results))
	connection.close()
	info = {}
	for key in dictionary:
		info[trans_wag[key]] = dictionary[key]
	return info


def profitability_info(date):
	global trans_prof
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM profitability WHERE date =:today', {'today': date})
	results = list(*cursor.fetchall())
	connection.close()
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
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

def get_user_email(user_id):
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	cursor = connection.cursor()
	cursor.execute('SELECT email FROM users WHERE user_id =:user_id_search', {'user_id_search': user_id})
	results = cursor.fetchall()
	connection.close()
	if len(results) > 0:
		return results[0][0]
	else:
		return 0

