from konlpy.tag import Okt
from collections import Counter
import pymysql
import mysql_user_info
import time

start_time = time.time()

# news 테이블에서 data 가져오기
def fetch():
    with pymysql.connect(db=user['db'], host=user['host'], user=user['user'], passwd=user['passwd'], port=user['port'], charset=user['charset']) as db:
        with db.cursor(pymysql.cursors.DictCursor) as cur:
            sql = 'SELECT * FROM news'
            cur.execute(sql)
            db.commit()

            data = cur.fetchall()

    return data

# morpheme 테이블에 data 넣기
def insert_data(id, type, word):
    with pymysql.connect(db=user['db'], host=user['host'], user=user['user'], passwd=user['passwd'], port=user['port'], charset=user['charset']) as db:
        with db.cursor() as cursor:
            sql = 'INSERT INTO morpheme (id, type, word) VALUES (%s, %s, %s)'
            cursor.execute(sql, (id, type, word))
            db.commit()

user = mysql_user_info.user_info
data = fetch()

# Okt 객체 선언
okt = Okt()

for i in range(25854):
    id = data[i]['publisher'] + '-' + data[i]['date']
    pos = okt.pos(data[i]['title'])
    noun = okt.phrases((data[i]['title']))

    for k in pos:
        if k[1] == 'adjective':
            insert_data(id, 'adjective', k[0])
        else :
            continue

    for k in noun:
        insert_data(id, 'noun', k)

# 실행 시간
print(f'Time : {time.time() - start_time}')