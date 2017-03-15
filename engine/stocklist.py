# -*- coding: utf-8 -*-
'''
	STOCK/ETF LIST UPDATER
'''
import csv
import xlrd

def read_company_list_from_csv(finame):

	rows = []
	try :
		f = open(finame, 'r')

		#read from csv
		for row in csv.reader(f):
			rows.append(row)

		f.close()

	except Exception as e:
		print e
		return None

	return rows


def read_etf_code_from_exel(filename):

	rows = []
	try:
		wb = xlrd.open_workbook(filename)
		ws = wb.sheet_by_index(0)

		num_col = ws.ncols
		num_row = ws.nrows

		for i in range(num_row):
			#print ws.row_values(i)[1] # Name
			#print ws.row_values(i)[2].strip('KRX:') # stock code
			rows.append([ws.row_values(i)[2].strip('KRX:') , ws.row_values(i)[1].strip()])
	
	except Exception as e:
		print e
		return None

	return rows

def update_etf():
	
	rows = read_etf_code_from_exel('./etf_code.xlsx')

	for row in rows:
	#	print row[0] + " | " + row[1]
		row.append(2) # type - 2 : ETF

	# get db instance
	from shdb import shdb_postgres
	db = shdb_postgres()
	table_name = db.make_stock_list_table_postgreSQL()

	# insert all data into stock list table 
	db.insert_data_postgreSQL(table_name, rows)

def update_companies():

	mod_rows = []

	# data retrieval from csv file 
	rows = read_company_list_from_csv('./company_list.csv')
	
	# re-arrange data array in order to put it in database
	if rows != None:
		#print rows[0] # <- 이것으로 하면 utf-8 표시가 제대로 되지 않
		#print repr(rows[0]).decode('string-escape')

		for i in xrange(1,len(rows)):
			row = rows[i]
			#zero_num = 6 - len(row[1])
			#print '0'*zero_num+row[1] + ' | ' + row[2]
			mod_rows.append(['0'*(6-len(row[1]))+row[1], row[2], 1])

	# get db instance
	from shdb import shdb_postgres
	db = shdb_postgres()
	table_name = db.make_stock_list_table_postgreSQL()

	# insert all data into stock list table 
	db.insert_data_postgreSQL(table_name, mod_rows)


def main():
	print "Create Stock List in stockhub database"

	update_companies()
	update_etf()
	

if __name__ == "__main__":
	main()
	
	

	


