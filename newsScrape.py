from bs4 import BeautifulSoup
import requests
import time
import pymysql
from datetime import datetime
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "news",
    "charset": "utf8"
}

start = time.time()
error=0

conn = pymysql.connect(**db_settings)

for id in range(1000000,2106724):
    
    try:
        #變數
        flag = 0
        flag2 = 0
        flag3=0
        category = ""
        keyword = ""
        keywords = ""
        keyArray = []
        names = ""
        name = []
        
        #設定url
        url = "https://www.ettoday.net/news/20211210/"+str(id)+".htm"
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        
        #ID
        print("\nID: ",id)
        
        #標題、時間
        title=soup.title.text
        for j in range(0,len(title)):
            if title[j] == "|":
                title = title[0:j].strip()
                print("Title: ",title)
                break

        posttime=soup.time.text.strip()
        list1=list(posttime)  

        for j in range(0,len(posttime)):
            if posttime[j] == "年" or posttime[j] == "月":
                list1[j] = "-"
            elif posttime[j] == "日":
                list1[j] = ""
            elif posttime[j] == ":":
                if flag3 != 1:
                    flag3+=1
                else:
                    list1 = list1[0:j]

        posttime=''.join(list1)
        posttimef = "%Y-%m-%d %H:%M"
        dposttime=datetime.strptime(posttime, posttimef)
        print("Time: ",dposttime)
        

        #記者
        result = soup.find_all("p")
        result = str(result)
        for j in range (0,len(result)):
            if result[j:j+2] == "記者":
                x=j
                for x in range (j,j+20):
                    if result[x:x+2] == "報導":
                        for k in range(j+2,x+2):
                            if result[k] != "／":
                                # if result[k]!= "、":
                                #     names += result[k]
                                # else:
                                #     name.append(names)
                                #     names = ""
                                names += result[k]
                            else:
                                # name.append(names)
                                names = names.strip()
                                print("Name: ",names)
                                flag=1
                                break
                        
                        if flag==1:
                            flag+=1
                            break

                if flag==2:
                    break


        #分類、關鍵字
        htmllist = r.text.splitlines()
        
        for row in htmllist:
            
            if "meta name=\"section\"" in row:
                
                for j in range(10,len(row)):
                    
                    if row[j:j+8] == "content=":
                        
                        for q in range(j+9,len(row)):
                            if row[q] == '"':
                                break
                            category += row[q]

                        print("Category: ",category)
                        flag2 += 1
                        break

            elif "meta name=\"news_keywords\" itemprop=\"keywords\"" in row:
                
                for j in range(20,len(row)):
                    
                    if row[j:j+8] == "content=":
                        
                        for q in range(j+9,len(row)):
                            if row[q] == '"':
                                break
                            keyword += row[q]

                        flag2 += 1
                        break
            
            elif flag2 == 2:
                break
        print("Keyword: ",keyword)


        #Link
        print("Link: ",url)

        
        #寫入sql     
        try:
            if names == '':
                names = '其他'
                
            
            with conn.cursor() as cursor:
                command = "INSERT INTO ettoday(ID, NAME, CATEGORY, TITLE, TIME, KEYWORD, LINK)VALUES(%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(command,(str(id),names, category, title, dposttime, keyword, url))
                conn.commit()
                
                print("success      error: ",error)
        except Exception as ex:
            error+=1
            print(ex)

        if soup.title.text=='找不到網頁':
            error+=1

    except:
        error+=1
        continue
print('\n\nerror:',error)

end = time.time()
print("time:",end - start)
