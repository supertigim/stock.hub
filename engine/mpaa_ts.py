# -*- coding: utf-8 -*-
'''
    TRADING STRATEGY - MODIFIED PAA
'''
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
#import pandas_datareader.data as web

matplotlib.rc('font', family='Malgun Gothic',size=8, weight = 'bold')

fd = pd.ExcelFile('./portfolio_data.xlsx')
portfolio = fd.sheet_names

# In[2]:

#2. 자산군별 데이터 프레임 설정

data = {}
for i in portfolio:
    data[i] = fd.parse(i)
    data[i].index = data[i].date
    data[i].drop('date', axis = 1, inplace=True)
    #print(u'num: '+i,len(data[i].columns))

# 월간 수익률
def m_return(dt):
    return dt / dt.shift(1)

'''
# 변동성대비모멘텀
def rel_momentum(dt):
    return (dt/dt.shift(12))/pd.rolling(12).std(dt)

# 연평균 수익률
def y_return(dt):
    return dt/dt.shift(12)
'''

# 평균모멘텀
def average_momentum(dt):
    mmt = 0
    for i in range(1, 13):
        mmt = dt / dt.shift(i) + mmt
    return mmt / 12

# 평균 모멘텀 스코어
def ammt_score(dt):
    ammt = average_momentum(dt).copy()
    #print ammt
    score = 0
    for i in range(1, 13):
        score = np.where(dt / dt.shift(i) > 1, 1, 0) + score
    ammt[ammt > -1] = score/12
    return ammt

# 현금혼합 모멘텀 수익 곡선
def cash_mixed_return_curve(dt, cash_rate=0.25):
    x = m_return(data['cash'])*cash_rate
    a = pd.DataFrame((m_return(dt).values*ammt_score(dt).shift(1).values+x.values)/(cash_rate+ammt_score(dt).shift(1).values)).cumprod() 
    a.index = dt.index
    a.columns = dt.columns
    return a

# 수익 곡선 모멘텀
def return_curve_mmt(dt):
    x = m_return(data['cash'])
    y = cash_mixed_return_curve(dt)
    a = pd.DataFrame((m_return(y).values*ammt_score(y).shift(1).values+(1-ammt_score(y).shift(1).values)*x.values)).cumprod() 
    a.index = dt.index
    a.columns = dt.columns
    return a

# 수익 곡선 순위
def return_curve_rank(dt, rk):
    x = average_momentum(return_curve_mmt(dt))
    y = x.iloc[ : , 0: len(x.columns)].rank(1, ascending=0)
    #print y
    y[y <= rk] = 1
    y[y > rk] = 0
    #print y
    return y

# 자산군 통합 포트폴리오
def asset_portfolio(dt, rk):
    x = m_return(return_curve_mmt(dt))
    y = return_curve_rank(dt, rk).shift(1)
    return ((x*y).sum(1)/(y.sum(1))).dropna().cumprod()

# 통합 모멘텀
def total_momentum():
    a = asset_portfolio(data['country'],3)
    b = asset_portfolio(data['sector'],5)
    c = asset_portfolio(data['factor'],2)
    d = asset_portfolio(data['bond'],1)
    e = pd.concat([a, b, c, d], axis=1)
    e.columns = ['country', 'sector', 'factor', 'bond']
    return e

# 최종 수익 곡선
def total_return_curve(cntr_r, sct_r, fct_r, bnd_r):
    x = m_return(total_momentum())
    y = ((x.country*cntr_r+x.sector*sct_r+x.factor*fct_r+x.bond*bnd_r)/(cntr_r+sct_r+fct_r+bnd_r)).cumprod()
    return y.dropna()
    
#4. 결과 plot
# 국가, 섹터, 팩터, 채권

a = total_return_curve(1,1,1,0)
#print a
b = data['country'].korea/data['country'].korea.ix[0]
c = pd.concat([a, b], axis=1).dropna()
c.columns = ['portfolio', 'kospi']
c.divide(c.ix[0]).plot(figsize =(8,6))
plt.show()

'''
#5. MDD
max_down = c.portfolio.rolling(min_periods=1, window = 500).max()
month_down = c.portfolio/max_down - 1.0
max_down_scale = month_down.rolling(min_periods=1, window=500).min()
month_down.plot(subplots=True, figsize = (7.8,2), linestyle='dotted')
max_down_scale.plot(subplots=True, figsize = (7.8,2), color = 'red', linestyle='dotted')
'''

plt.show()
