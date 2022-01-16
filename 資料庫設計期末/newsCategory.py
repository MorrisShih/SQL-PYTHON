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

    #這邊先總共有甚麼類別
    command = "SELECT `CATEGORY` FROM news.ettoday group by `CATEGORY`;"
    cursor.execute(command)
    result = cursor.fetchall()

    category = []
    

    print(type(result[0][0]))
    for  i in range(len(result)):
        category.append(result[i][0])
    print(category)
    
    #搜尋寫過此類別的記者
    for i in range(len(category)):
        
        command = "SELECT `NAME` FROM news.ettoday WHERE `CATEGORY` = \""+str(category[i])+"\";"
        cursor.execute(command)
        result = cursor.fetchall()
        name = []
        num = []
        num1 = 0
        num2 = 0

        #這邊主要是將記者做紀錄
        for j in range(len(result)):
            num2 += 1

            #將其它排除掉，其它項是從別的網站節錄的新聞或是未署名記者
            if result[j][0] == "其它":
                num1 += 1

            else:
                #有可能一篇有1~3個記者，將其作分類並記錄
                if "、" in str(result[j][0]):
                    n = str(result[j][0]).split("、")

                    for k  in range(len(n)):

                        if n[k] not in name:
                            name.append(str(n[k]))
                            num.append(1)

                        else:
                            num[name.index(n[k])] += 1
                    
                else:
                    if str(result[j][0]) not in name:
                        name.append(str(result[j][0]))
                        num.append(1)

                    else:
                        num[name.index(str(result[j][0]))] +=1
        
        #泡沫排序法，將最大的抓出
        for j in range(len(num) - 1):
            if num[j] > num[j + 1]:
                num[j], num[j + 1] = num[j + 1], num[j]
                name[j], name[j + 1] = name[j + 1], name[j]

        s=str(category[i]) + " --> " + str(name[-1]) + "   撰寫篇數 : " + str(num[-1]) + "   其它篇章節錄數 : " + str(num1) + "   該類別總文章數 : " + str(num2)
        
        print(s)
        
