import requests
import timeit
import urllib.request
import urllib.parse
import html5lib # pip install html5lib
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv


def searchengine(search):
    results = 10
    robo=False
    page = requests.get("https://www.google.com/search?q={}&num={}".format(search, results))
    soup = BeautifulSoup(page.content, "html5lib")
    links = soup.findAll("a")
    finalresult=[]
    for link in links :
        link_href = link.get('href')
        if link_href=="//www.google.com/policies/terms/":
            robo=True
            break
        if "url?q=" in link_href and not "webcache" in link_href:
            result=link.get('href').split("?q=")[1].split("&sa=U")[0]
            if result.startswith("http") or result.startswith("fpt"):
                    finalresult.append(result)
    if robo:
        results = 10
        finalresult=[]
        page = requests.get("https://www.bing.com/search?q={}&count={}".format(search, results))
        soup = BeautifulSoup(page.content, "html5lib")
        litags = soup.findAll('li',attrs={"class":"b_algo"})
        for link in litags :
            anchor = link.find('a')
            link_href = anchor.get('href')
            finalresult.append(link_href)
    return finalresult
#--------------------------------------------------------------------------------------------
def keywordsresults(arr):
        title=[]
        temp=[] # temporary value hold karne k liye
        relativelink=[]
        try:
                DatabaseCheck = open('mainapp/database/database.csv')
                DatabaseReader = csv.reader(DatabaseCheck)
                DatabaseData = list(DatabaseReader)
        except:
                DatabaseData=[]
        for search in arr:
                flag=0
                title.append(search)
                for item in DatabaseData:
                    if item[0]==search:
                        for i in range(1,len(item)):
                            if item[i]!='':
                                flag = 1
                                temp.append(item[i])
                                if len(temp)==5:
                                    break
                if flag == 1:
                    relativelink.append(temp)
                    temp=[]
                if flag==0:
                        robo=False #google error
                        #result = 10
                        temp.append(search)
                        page = requests.get("https://www.google.com/search?q={}&num=10".format(search))
                        soup = BeautifulSoup(page.content, "html5lib")
                        links = soup.findAll("a")
                        for link in links :
                                link_href = link.get('href')
                                if link_href=="//www.google.com/policies/terms/":
                                    robo=True
                                    break
                                if "url?q=" in link_href and not "webcache" in link_href:
                                        result=link.get('href').split("?q=")[1].split("&sa=U")[0]
                                        if result.startswith("http") or result.startswith("fpt"):
                                                temp.append(result)
                        if robo:
                            page = requests.get("https://www.bing.com/search?q={}&count=10".format(search))
                            soup = BeautifulSoup(page.content, "html5lib")
                            litags = soup.findAll('li',attrs={"class":"b_algo"})
                            for link in litags :
                                anchor = link.find('a')
                                link_href = anchor.get('href')
                                temp.append(link_href)
                        if len(temp)==1:
                            relativelink.append(["No any result found"])
                        else:
                            relativelink.append(temp[1:])
                            with open(r'mainapp/database/database.csv', 'a',encoding='utf-8', newline='') as f:
                                    writer = csv.writer(f)
                                    writer.writerow(temp)
        final_result_solution=zip(title,relativelink)
        return final_result_solution
