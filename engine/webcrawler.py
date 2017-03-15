# -*- coding: utf-8 -*-
'''
	WEB CRWALER for STOCK DATA 
'''
import requests
from bs4 import BeautifulSoup
from datetime import date

MAX_PAGES = 200
#MAX_PAGES = 1

#DEF_STOCK_CODE = '079550' # LIG NextOne
#DEF_STOCK_CODE = '005930' # Samsung Electoring
DEF_STOCK_CODE = '089850' # ubivelox
#DEF_STOCK_CODE = '204480' # Tiger China 'A' Leverage

# Gather Each Stock History in Naver Finance
def nf_stock_history(stock_code = DEF_STOCK_CODE, max_pages = MAX_PAGES) :
	rows = []

	page = 1 
	last_page = None
	is_complited  = False 
	
	while page <= max_pages:
		url = 'http://finance.naver.com/item/frgn.nhn?code=' + stock_code + '&page=' + str(page)
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text, 'lxml')
		
		# find tbody with those attributes
		table = soup.find_all('tr', {"onmouseover": "mouseOver(this)",
			"onmouseout": "mouseOut(this)"})

		for tr in table:
			#print "\n"
			#print "#"*50
			row = []
			for td in tr.find_all('td'):

				data = td.text.strip()

				if data == "":
					#print "Empty column is found"
					is_complited = True
					break

				row.append(data)
				#print data
				# data[0] - Date
				# data[1] - Close 
				# data[2] change 
				# data[3] change by percentage
				# data[4] Total Volume
				# data[5] Volume by Firms
				# data[6] Volume by Foreigners
				# data[7] Stock Share to Foreigners
				# data[8] Stock Share to Foreigners by Percentage

			if is_complited == True:
				break
			rows.append(row)

		# find last page for stopping loop
		if last_page == None:
			# Among A href, number of last page can be found
			last_page = soup.find('td', {"class": "pgRR"}).a['href']
			# split the text with "=" and retrive last one
			last_page = int(last_page.split("=")[-1])
		else:
			if last_page == page:
				is_complited = True

		if is_complited == True:
			#print "Crawling is done!!!\n"
			break;

		page = page + 1

	return stock_code, rows

def update_stock_history_on_db(stock_name):

	from shdb import shdb_postgres
	 
	db = shdb_postgres()

	# 종목 코드 추출 
	code = db.retrieve_stock_code(stock_name)

	# 종목 크롤링 
	code, stock_rows = nf_stock_history(code)

	# 데이터 정렬
	rows = []
	for row in stock_rows:
		#print row[0] + " | " + row[1]  + " | " +  row[4]  + " | " +  row[5]  + " | " + row[6]
		
		dt = row[0].replace(".","-")
		close = int(row[1].replace(",", ""))
		vol = int(row[4].replace(",", ""))
		vol_firm = int(row[5].replace(",", ""))
		vol_foreigner = int(row[6].replace(",", ""))

		rows.append([dt, close, vol, vol_firm, vol_foreigner])

	# 개별 종목 테이블 생성 
	table_name = db.make_stock_history_table_name(code)
	db.make_stock_history_table_postgreSQL(table_name)

	
	# DB 업데이트 
	db.insert_data_postgreSQL(table_name, rows)


def test():
	import time
	start_time = time.time()
	code, stock_rows = nf_stock_history()
	end_time = time.time()
	print "종목번호 : " + code 
	print "총 데이터 길이 : " + str(len(stock_rows))
	print "크롤링 시간 : " + str(end_time - start_time)


def main():
	#test()

	print "Crawling Data from Web"
	update_stock_history_on_db('삼성전자')	


if __name__ == "__main__":

	main()
	




