import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Aqzk1230723",
    "db": "news",
    "charset": "utf8"
}

conn = pymysql.connect(**db_settings)

with conn.cursor() as cursor:

    #輸入姓名、日期
    name = input("輸入姓名 : ")
    print("輸入年月日(2017-08-29 -> 2021-10-22)")
    y = input("年 : ")
    m = input("月 : ")
    d = input("日 : ")

    ymd = y+"-"+m+"-"+d
    command = "SELECT * FROM news.ettoday WHERE NAME LIKE \'%"+name+"%\' AND TIME BETWEEN '"+ymd+" 00:00' AND '"+ymd+" 23:59';;"
    cursor.execute(command)
    result = cursor.fetchall()

    #印出此記者在其日期的新聞
    for i in range(len(result)):
        for j in range(len(result[i])):
            print(result[i][j])

        print("\n")
    
    if result == ():
        print("無此記者或此記者當日無新聞")
