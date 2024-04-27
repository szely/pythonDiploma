import sqlite3

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
	# for row in results:
	# 	print(row[0])
	connection.close()
	return results[0][0]

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
	n = {}
	for key in dictionary:
		n[trans[key]] = dictionary[key]
	return n



	# def update_sqlite_table():
	# 	try:
	# 		sqlite_connection = sqlite3.connect('sqlite_python.db')
	# 		cursor = sqlite_connection.cursor()
	# 		print("Подключен к SQLite")
	#
	# 		sql_update_query = """Update sqlitedb_developers set salary = 10000 where id = 4"""
	# 		cursor.execute(sql_update_query)
	# 		sqlite_connection.commit()
	# 		print("Запись успешно обновлена")
	# 		cursor.close()
	#
	# 	except sqlite3.Error as error:
	# 		print("Ошибка при работе с SQLite", error)
	# 	finally:
	# 		if sqlite_connection:
	# 			sqlite_connection.close()
	# 			print("Соединение с SQLite закрыто")
	#
	# update_sqlite_table()

# dict  = find_wagon(28068724)
#
# for key,value in dict.items():
# 	print(key, ':', value)

#
#
# connection = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database')
# connection.row_factory = sqlite3.Row
# cursor = connection.execute('select * from wagons')
# # instead of cursor.description:
# row = cursor.fetchone()
# names = row.keys()
# print(names)
#
# dictionary = dict(zip(names, find_wagon(28068724)))
# print(dictionary)

# trans = {'id': 'id', 'wagon_number': 'Номер вагона', 'wagon_type': 'Род вагона', 'wagon_subtype': 'Подрод вагона', 'wagon_model': 'Модель вагона', 'construction_date': 'Дата постройки', 'wagon_end_date': 'Срок службы', 'wagon_supplier': 'Поставщик', 'client': 'Клиент', 'business_activity_typ': 'Вид деятельности'}
# n = {}
# for key in dictionary:
# 	n[trans[key]] = dictionary[key]
# print(n)