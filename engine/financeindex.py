# -*- coding: utf-8 -*-
'''
	GATHERING GLOBAL FINANCE INDEX 
'''
#import time
#import math
#import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import pandas_datareader.data as web

def isMonthEndforStock(date):
	date = datetime(date.year, date.month, date.day, 0 ,0 , 0)
	
	modDate = date + pd.offsets.MonthEnd(0)
	wd = modDate.weekday()

	# Saturday or Sunday
	if( wd > 4):
		modDate = date - timedelta(days=(6-wd))
	
	return (modDate == date), modDate

def find_last_day_of_each_month():

	dt = datetime(2016,7,29)
	print isMonthEndforStock(dt)

def gather_month_end_stock_val():
	#start = dt.datetime(2016,11,7)
	start = datetime(2016,10,7)
	end = date.today()

	# Google 
	Data_Source = 'google'
	Close_Col = 'Close'		

	# Yahoo 
	#Data_Source = 'yahoo'
	#Close_Col = 'Adj Close'	# when 'yahoo'

	Fianance_Index = ['KOSPI']
	num_stocks = len(Fianance_Index)

	f = web.DataReader(Fianance_Index,
	                   Data_Source,
	                   start,
	                   end)

	cleanData = f.ix[Close_Col]
	print cleanData
	closeData = pd.DataFrame(cleanData)
	closeData.fillna(method='backfill', inplace=True)

	cleanData = f.ix['Volume']
	#print cleanData

	volumeData = pd.DataFrame(cleanData)
	volumeData.fillna(method='backfill', inplace=True)

	for indexName in Fianance_Index:
		print indexName + '\n'					# index name

		print 'Last data of the month: '
		for i in xrange(1, len(closeData[indexName])):	
			if closeData[indexName].index[i].month != closeData[indexName].index[i-1].month:
				print closeData.index[i-1]			# date
				print closeData[indexName][i-1]		# close
				print volumeData[indexName][i-1]	# volume
				print '\n'

			if i == (len(volumeData[indexName]) - 1) and float(volumeData[indexName][i]) != 0.0:
				if isMonthEndforStock(volumeData[indexName].index[i]):
					print closeData.index[i]		# date

if __name__ == "__main__" :
	gather_month_end_stock_val()
	#find_last_day_of_each_month()



