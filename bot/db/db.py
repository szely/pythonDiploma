import sqlite3

# conn = sqlite3.connect('/Users/a1234/PycharmProjects/pythonDiploma/bot/db/database', check_same_thread=False)
# cursor = conn.cursor()
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