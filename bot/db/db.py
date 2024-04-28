import sqlite3
import pandas

trans = {'id': 'id', 'wagon_number': 'Номер вагона', 'wagon_type': 'Род вагона', 'wagon_subtype': 'Подрод вагона', 'wagon_model': 'Модель вагона', 'construction_date': 'Дата постройки', 'wagon_end_date': 'Срок службы', 'wagon_supplier': 'Поставщик', 'client': 'Клиент', 'business_activity_typ': 'Вид деятельности'}
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
	if len(results) > 0 :
		return results[0][0]
	else:
		return 0
	connection.close()

def find_wagon(number):
	global trans
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
		info[trans[key]] = dictionary[key]
	return info

def profitability_info():
	connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
	cursor = connection.cursor()
	cursor.execute('SELECT user_id FROM users WHERE user_id =:user_id_search', {'user_id_search': user_id})
	results = cursor.fetchall()
	# for row in results:
	# 	print(row[0])
	connection.close()
	return results[0][0]

# print(find_user_id(1071020716))

