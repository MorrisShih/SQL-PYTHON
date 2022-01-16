import pymysql
import matplotlib.pyplot as plt

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


    #輸入年月日
    print("輸入年月日(2017-08-29 -> 2021-10-22)")

    y = input("年 : ")
    m = input("月 : ")
    d = input("日 : ")

    ymd = y+"-"+m+"-"+d

    command = "SELECT `ID`,`TITLE`,`TIME`,`KEYWORD`,`LINK` FROM news.ettoday WHERE TIME BETWEEN '"+ymd+" 00:00' AND '"+ymd+" 23:59';"
    cursor.execute(command)
    result = cursor.fetchall()
    
    #輸出當日新聞
    for i in range(len(result)):

        for j in range(5):
            print(result[i][j])

        print("\n")

    #這邊重新抓取一次只有KEYWORD的資料
    command = "SELECT `KEYWORD` FROM news.ettoday WHERE TIME BETWEEN '"+ymd+" 00:00' AND '"+ymd+" 23:59';"
    cursor.execute(command)
    result = cursor.fetchall()

    keywords = []
    num = []

    #這邊是將抓到的資料做比對，若沒出現過的keywords會新增，並在相對位置的num添加
    #若已出現過，則將在相對位置的num的數字+1
    for i in range (0,len(result)):
        print("計算中..."+str(i))

        for j in range (0,len(result[i])):

            if result[i] == ('',):
                break

            keyword = str(result[i][j]).split(",")
            
            for k in range(0,len(keyword)):

                if keyword[k] != '':
                    if keyword[k] in keywords:
                        num[keywords.index(keyword[k])] += 1

                    else:
                        keywords.append(keyword[k])
                        num.append(1)


    #泡沫排序，比10次，比完10次後，最後10項即為最大的10個
    for i in range(10):

        for j in range(len(num) - 1 - i):
            print("計算中..."+str(j))

            if num[j] > num[j + 1]:
                num[j], num[j + 1] = num[j + 1], num[j]
                keywords[j], keywords[j + 1] = keywords[j + 1], keywords[j]
    
    #因為電腦的問題，無法印出中文，故以ABC代替，並在底下生成ABC對應文字
    lable = ['A','B','C','D','E','F','G','H','I','K']
    keywordsTop10 = keywords[-10:len(keywords)]
    numTop10 = num[-10:len(num)]
    lables = []

    for i in range(10):
        lables.append(str(lable[i])+"="+str(numTop10[i]))

    for i in range(10):
        print(lable[i] + " = " + keywordsTop10[i] + " = " + str(numTop10[i]))

    #印出圓餅圖
    plt.title(ymd+" KEYWORD TOP10")
    plt.pie(numTop10 , labels=lables,autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()
