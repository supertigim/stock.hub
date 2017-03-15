# -*- coding: utf-8 -*-
'''
	STOCK HUB DATABASE HANDLER
'''
import psycopg2 as pg2

DEF_HOST = 'localhost'
DEF_DB_NAME = "postgres"
DEF_USER = "postgres"
DEF_PSWD = "1111"

DEF_STOCK_HUB_DB_NAME = 'stockhub'

TABLE_STOCK_LIST = 'stocklist'
TABLE_STOCK_LIST_ATTS = 'code varchar(6) primary key, Name varchar(50), type integer'

TABLE_STOCK_HISTORY_ATTS = 'date date primary key, close integer, volume bigint, volbyfirm bigint, volbyforeigner bigint'

# Class : Stock.Hub Database on PostgreSQL 
class shdb_postgres:
	conn = None
	cur = None
	db = None

	def __init__(self, url = DEF_HOST, db_name = DEF_STOCK_HUB_DB_NAME, user = DEF_USER, pswd = DEF_PSWD):
		try:
			self.db = db_name

			query = 'host=' + url + ' dbname=' + db_name + ' user=' + user + ' password=' + pswd
			#print query

			self.conn = pg2.connect(query)

			self.conn.autocommit = True
			self.cur = self.conn.cursor()

		except Exception as e:
			print 'postgresql database connection error!'
			print e
		
	def __del__(self):
		if self.cur:
			self.cur.close()

		if self.conn:
			self.conn.close()

	# database 만들기 
	def create_db(self, name):
		if self.conn == None or self.cur == None:
			return

		try:
			query = 'create database ' + name
			self.cur.execute (query)
		except Exception as e:
			print e

	# create table
	def make_table_poestgreSQL(self, table_name, table_attrs):
		if self.conn == None or self.cur == None:
			return

		try:
			query = 'CREATE TABLE ' + table_name +' (' + table_attrs + ' )' 
			self.cur.execute(query)
		except Exception as e:
			print e

	def insert_data_postgreSQL(self, table_name, rows):
		if self.conn == None or self.cur == None:
			return

		try:
			# insert data
			for row in rows:
				query = "INSERT INTO " + table_name + " VALUES("

				size = len(row)
				for col in row:
					size -= 1

					if isinstance(col, int):
						query += `col`			# into string 
					else:
						query += "'" + col + "'" # needs semicolon both sides

					if size:
						query += ","
					
				query +=  ")"

				#print query
				self.cur.execute(query)

			#self.cur.fetchall()

		except Exception as e:
			print e

	def retrieve_stock_code(self, name) :
		if self.conn == None or self.cur == None or self.db != DEF_STOCK_HUB_DB_NAME:
			return

		try:
			# insert data
			query = "SELECT code FROM " + TABLE_STOCK_LIST + " WHERE name = '" + name + "'"
			#print query

			self.cur.execute(query)
			#rows = self.cur.fetchall()
			rows = self.cur.fetchone()
			return rows[0]		# because code is primary key

		except Exception as e:
			print e

	####### Additional Methods for easier usasge #####################

	def make_stock_history_table_name(self, stock_code):
		table_nam = '_' + stock_code + '_history_'
		return table_nam

	def make_stock_history_table_postgreSQL(self, table_name):
		self.make_table_poestgreSQL(table_name,TABLE_STOCK_HISTORY_ATTS)

	def make_stock_list_table_postgreSQL(self):
		self.make_table_poestgreSQL(TABLE_STOCK_LIST,TABLE_STOCK_LIST_ATTS)
		return TABLE_STOCK_LIST

# end of class : shdb_postgres

# create stockhub database 
def create_stock_hub_database():
	db = shdb_postgres(DEF_HOST, DEF_DB_NAME)
	db.create_db(DEF_STOCK_HUB_DB_NAME)

# for test
def main():

	# [1] stockhub 데이터베이스 생성
	#create_stock_hub_database()

	# [2] stocklist table 생성
	#db = shdb_postgres()
	#db.make_stock_list_table_postgreSQL()

	# [3] 종목 코드 찾기
	#db = shdb_postgres(DEF_HOST, DEF_STOCK_HUB_DB_NAME)
	#print db.retrieve_stock_code('케이티')
	#print db.make_stock_history_table_name(db.retrieve_stock_code('케이티'))

	# [4] 종목별 히스토리 테이블 생성
	#db = shdb_postgres(DEF_HOST, DEF_STOCK_HUB_DB_NAME)
	#tb_name = db.make_stock_history_table_name(db.retrieve_stock_code('케이티'))
	#db.make_table_poestgreSQL(tb_name,TABLE_STOCK_HISTORY_ATTS)

if __name__ == "__main__":
	main()
