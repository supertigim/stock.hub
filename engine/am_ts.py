# -*- coding: utf-8 -*-
'''
	TRADING STRATEGY - ADAPTIVE MOMENTUM
'''

import pandas as pd
#import matplotlib.pyplot as plt
#matplotlib.use('qt4agg') 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import numpy as np 
import pandas_datareader.data as web 

def shist(stock_name, start_date, pr = 'day'):

	# Google 
	#source = 'google'
	#closeColumnName = 'Close'	

	# Yahoo 
	source = 'yahoo'
	closeColumnName = 'Adj Close'	

	sh = web.DataReader(name = stock_name, data_source= source, 
						start = start_date)[closeColumnName]

	# day
	if pr == 'day':
		return sh.div(sh.iat[0]).to_frame('sh')

	if pr == 'month':
		# 첫째 일 종가 기준으로 나눈, 매달 마지막 일의 지수를 'sh' column에 저장 
		# sh : stock history
		return sh.div(sh.iat[0]).resample('M').last().to_frame('sh')
	#if pr == 'week':
	else: 
		# 첫째 일 종가 기준으로 나눈 매주 금요일의 지수 검색 범 
		return sh.div(sh.iat[0]).resample('W-FRI').last().to_frame('sh')

def adjust_period(data, period, dynamic = True):
	df = pd.DataFrame()

	# 절대값 
	data['abs_val'] = data['sh'].diff(period).abs()
	# 상대값 
	data['rel_val'] = data.sh.diff().abs().rolling(period).sum()
	if dynamic:		
		#가변주기
		data['period'] = (data['abs_val']/data['rel_val']*period).dropna().astype(int) 
	else:
		#고정주기로 하고 싶으면, 
		data['period'] = period

	df = pd.concat([df, data['period']], axis=1)
	return df

##### for google finance ##############
#stock = shist('KOSPI', '2004-01-01', 'month')
#stock = shist('SX5E', '2004-01-01', 'month')

##### for yahoo finance ############### 
stock = shist('^KS11', '2001-01-01', 'month')
#stock = shist('^KS11', '2001-01-01', 'day')
#stock = shist('^DJI', '2001-01-01', 'day')
#stock = shist('^DJI', '2001-01-01', 'month')

#stock = shist('^GSPC', '2001-01-01', 'month')
#stock = shist('005930.KS', '2015-01-01', True) #삼성 전자
#print stock

# 최대 가변 주기 적용 (예, 3/6/9 개월 or 주 or 일) 
# day일 경우, 3일 가변이 최적
#stock['period'] = adjust_period(stock, 3, True)
# month 일 경우, 12개월 가변이 최적
stock['period'] = adjust_period(stock, 12, True)
stock.dropna(inplace = True)

# 'period'이전의 'sh' 컬럼 값을 'd_mo' 컬럼에 저장
#  ex) period:3이면, stock['d_mo'] = stock['sh'][현재위치-3]
def adaptive_momentum(x):
	return stock['sh'].shift(x['period'])[x.name]
stock['d_mo'] = stock.apply(adaptive_momentum, axis=1)

# 'sh' 보다 'd_mo'가 크면, 추세라고 판단하고 보유, 아니면, 매도(의미는 현금--> 03**(1/12))
stock['profit'] = np.where(stock.sh.shift(1)>stock.d_mo.shift(1), stock.sh/stock.sh.shift(1) , 1.03**(1/12)).cumprod()
#stock['signal'] = np.where(stock.sh.shift(1)>stock.d_mo.shift(1), 1.5,1)
# 현금 비중을 반으로 했을 경우 현금 이율은 년 3%로 예상 (단기 채권)
#stock['mix_invest'] = np.where(stock.sh.shift(1)>stock.d_mo.shift(1), (stock.sh/stock.sh.shift(1)+1.03**(1/12))/2 ,1).cumprod()

print stock

# 시작일 대비로 주가 표현 : 1보다 크면 상승, 작으면 하락 | 회색으로 표현 
(stock.sh/stock.sh.ix[0]).plot(color="gray")
stock.profit.plot(color="red")
#stock.mix_invest.plot(color="green")

plt.show()


