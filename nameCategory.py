import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "news",
    "charset": "utf8"
}

conn = pymysql.connect(**db_settings)

with conn.cursor() as cursor:
    #輸入姓名
    while True:
        name = input("輸入姓名 : ")

        command = "SELECT `CATEGORY` FROM news.ettoday WHERE NAME LIKE \'%"+name+"%\';"
        cursor.execute(command)
        result = cursor.fetchall()

        if result == ():
            print("無此記者......")
        else :
            break

    category = []
    num = []

    #這邊是將類別作數量登記
    for i in range(len(result)):
        
        if result[i][0] not in category:
            category.append(result[i][0])
            num.append(1)
        
        else:
            num[category.index(result[i][0])] +=1

    #這邊做泡沫排序由小排到大
    for i in range(len(num)-1):

        for j in range(len(num) - 1 -i):
            
            if num[j] > num[j + 1]:
                num[j], num[j + 1] = num[j + 1], num[j]
                category[j], category[j + 1] = category[j + 1], category[j]
    
    #印出排序過的資料
    for i in range (len(category)):
        print(category[i]+" : "+str(num[i]))
