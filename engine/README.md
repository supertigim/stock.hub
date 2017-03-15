## 환경 세팅  
  
python2.7과 pip 설치. IDE는 주로 PyCharm이나 Sublime Text사용
PostgreSQL는 호스트에 설치 되어 있는 것으로 가정  
  
우분투의 경우, 
  
	sudo apt-get install python-pip python-dev  
 
### Python 가상 환경을 위한 모듈   
  
PC 및 OS에 독립적인 실행 환경 제공. Devops 최적  
 
	sudo pip install --upgrade pip  
	sudo pip install virtualenv  
	sudo pip install virtualenvwrapper  
  
### 가상 개발 환경 생성 및 사용   

	// virtualenv 관련 파일을 저장하기 위한 디렉토리 및 실행 파일 export  
	$ mkdir ~/.virtualenvs  
	$ vi ~/.bashrc 파일 끝에  
	  export WORKON_HOME=~/.virtualenvs  
	  source /usr/local/bin/virtualwrapper.sh  
	  :wq  
	  
	// 가상 개발 생성 및 사용하기
	$ source ~/.bashrc  	== bash 로드   
	$ mkvirtualenv py_study == 가상개발영역 만들기
	(py_study) $ deactivate == 가상영역 빠져 나오기

	// 새로운 터미널에서 실행시 
	$ source ~/.bashrc  	== bash 로드   
	$ workon py_study       == 가상영역으로 들어가기

	//기타 기능 
	$ source ~/.bashrc  	== bash 로드   
	$ cdvirtualenv          == 가상영역 디렉토리로 이동
	$ wipeenv               == 현재 가상환경의 써드파티 패키지 전체 삭제
	$ workon                == 가상환경 목록
	$ rmvirtualenv          == 가상환경 삭제

### 프로젝트용 개발 환경 세팅 방법 (예시)
  
	# Virtual 개발 환경 생성   
	$ source ~/.bashrc  										== bash 로드  
	$ mkvirtualenv stock 										== 가상개발영역 만들기   
  
	# File 설치 및 환경 설정  
	(stock) $ mkdir trading_engine								== 디렉토리 생성  
	(stock) $ cd trading_engine									== 이동  
	(stock) trading_engine $ git pull site_XXXX					== git에서 파일 가져오기  
	
	### Dependancy 모듈 설치 하기 ###
	# PostgreSQL이 설치되어 있어야 하며, 아래 패스를 미리 설정해 두어야 한다. 
	# export PATH=$PATH:/Library/PostgreSQL/9.5/bin)  
	   
	(stock) trading_engine $ pip install -r requirements.txt 	== Dependancy 모듈 설치  
  
 	# Test  
	(stock) trading_engine $ python shdb.py  
  
## 전체 설명 

종목(ETF 포함) 이름과 코드는 증권 거래소에서 가져오고, 각 종목 및 시장 Index값은 Web Crawling으로 생성 
DB는 하나를 생성하며, 종목 리스트를 위한 테이블, 각 종목 별 테이블을 생성하여 업데이트. 추후 시장 인덱스 값을 위한 인덱스 리스트 및 인덱스 별 테이블을 구성할 예정  

(그림 삽입)  

## 파일 설명 

### [1] shdb.py (Stock Hub Database Handler)

postgreSQL과 MongoDB(아직 안함. 2016/12/19) 연결용 Wrapper Class  
  
	from shdb import shdb_postgres  
  
	# [1] stockhub 데이터베이스 생성  
	db = shdb_postgres()  
	db.create_db(DEF_STOCK_HUB_DB_NAME)  
  
	# [2] stocklist table 생성  
	db = shdb_postgres(DEF_HOST, DEF_STOCK_HUB_DB_NAME)  
	db.make_table_poestgreSQL(TABLE_STOCK_LIST,TABLE_STOCK_LIST_ATTS)  
  
	# [3] 종목 코드 찾기  
	#db = shdb_postgres(DEF_HOST, DEF_STOCK_HUB_DB_NAME)  
	#print db.retrieve_stock_code('케이티')  
	#print db.make_stock_history_table_name(db.retrieve_stock_code('케이티'))  
  
	# [4] 종목별 히스토리 테이블 생성  
	#db = shdb_postgres(DEF_HOST, DEF_STOCK_HUB_DB_NAME)  
	#tb_name = db.make_stock_history_table_name(db.retrieve_stock_code('케이티'))  
	#db.make_table_poestgreSQL(tb_name,TABLE_STOCK_HISTORY_ATTS)  

### [2] webcrawler.py (Stock Data Web Crwaler)  
  
TBD   

### [3] stocklist.py (Stock/ETF/Inex List Updater)
  
TBD  
  
  
## To-Do List (2016.12.19)

1. 매일 업데이트 하는 로직
2. 마켓 인덱스 리스트 및 히스토리 테이블 생성
3. deep learning interface methods in shdb class  
4. deep learning study
  
  
## License
MIT
  
  
## Reference 

1. postgresql 접속하기 - http://freeprog.tistory.com/100  
2. pandas 매주 종가 구하기 - http://stackoverflow.com/questions/34597926/converting-daily-stock-data-to-weekly-based-via-pandas-in-python
3. MACD/BB/이평선 구하기 - https://github.com/sparrowapps/systemt/blob/master/analyze.py
4. RSI 구하기 - https://github.com/mtamer/python-rsi/blob/master/Stock%20Screener/rsi.py
5. matplotlib 에서 finance관련 - http://matplotlib.org/examples/pylab_examples/finance_work2.html
6. 초등학생도 복리 40% - https://www.snek.ai/alpha/article/108117/%EC%B4%88%EB%93%B1%ED%95%99%EC%83%9D-%EA%B3%A0%ED%95%99%EB%85%84%EC%9D%B4-%EB%B3%B5%EB%A6%AC-25-%EB%B2%8C-%EC%88%98-%EC%9E%88%EB%8A%94-%EB%B0%A9%EB%B2%95
7. 여려 조건으로 종목 검색 - http://comp.fnguide.com/svo/Kdbdw/screener.asp?u=xxx#tabPaging

