from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
from wsgiref.util import FileWrapper
#from .searchengine import *
from .nonrelevent import *
from time import *
import os
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, 
    PageTemplate, 
    Frame, 
    Paragraph
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow,
    blue
)
global problem_statement
#-----------------------------------------------------------------------------------------------------------
def index(request):
    try:
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except:
        client_address = request.META['REMOTE_ADDR']
    print("User with ip connected "+client_address+" at "+ctime())
    return render(request,'final.html')
#-----------------------------------------------------------------------------------------------------------
def searchbox(request):
    if request.method == 'POST':
            searchitem = request.POST['searchget']
            result=searchengine(searchitem)
            #print(result)
            if len(result)==0:
                result.append("No any result found")
            return render(request,'search.html',{'search':searchitem,'links':result})
    return render(request, 'search.html', {'search':"Enter search in searchbox and hit enter"})
#------------------------------------------------------------------------------------------------------------
def challenges(request):
    myhref=list()
    mytitle=list()
    url = urllib.request.urlopen('http://www.tatainnoverse.com')
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find_all('div',{'class':'content'})
    for x in table:
        anchor = x.find('a',href=True)
        if 'challenge.php?id=' in anchor['href']:
            y=anchor['href']
            z=anchor.text
            myhref.append(y)
            mytitle.append(z)
    main=zip(mytitle,myhref)
    #print(main)
    return render(request,'challenge.html',{'main':main})
#------------------------------------------------------------------------------------------------------------
def problemstatement(request): #proble html
    global problem_statement
    problemlink = request.GET.get('title_name')
    start = 'https://www.tatainnoverse.com/'
    link = start+problemlink
    url = urllib.request.urlopen(link)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.findAll('div',attrs={"id":"singlechallengedesc"})
    problem_statement=table[0].text
    return render(request,'problemstatement.html',{"problem_statement":problem_statement})    
#-----------------------------------------------------------------------------------------------------------
def keywords(request):
    global form
    global problem_statement
    temp=[]
    ans=[]
    temp=list(set(list(problem_statement.split()))) # It will remove all similar elements
    for i in temp:
            if not i.isalpha():
                    pass
            else:
                tempk=i.lower()
                if tempk in non_relevent[tempk[0]]:
                    pass
                else:
                    ans.append(i)
    return render(request, 'keyword.html', {'keys': ans})
#-----------------------------------------------------------------------------------------------------------
def solution(request):
    try:
        os.unlink("log.pdf")
    except:
        pass
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=15,
            leading=22,
            leftIndent=-13,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=12,
            bulletIndent=0,
            textColor= blue,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform='lowercase',  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
            
        ),
    }

    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=purple,
        textTransform='uppercase',
    )
    styles['keyword'] = ParagraphStyle(
       'link',
        parent=styles['default'],
        fontSize=13,
        leading=22,
        textColor=black,
        textTransform='uppercase',
        
    )

#styles[Normal] styles[Bullet]
    
##################################################################################################
    if request.method == 'POST':
        data = request.POST['workb']
        arr=data.split(',')
        result=keywordsresults(arr)
        resultdict=dict(keywordsresults(arr))
        #print(resultdict)
        doc = SimpleDocTemplate("log.pdf",pagesize=landscape(letter),
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)

        Result=[]
        ptext = "Problem Solution"
        Result.append(Paragraph(ptext,styles["title"]))
        for i,j in resultdict.items():
            ptext = '<br/>KEYWORD: '+i
            Result.append(Paragraph(ptext,styles["keyword"]))
            ptext=""
            for x in j:
                ptext='<bullet>&bull;</bullet><u>'  + x+ '<br/></u>'
                Result.append(Paragraph(ptext,styles["default"]))
        doc.build(Result)

        return render(request, 'solution.html', {"main":result})
    return render(request,'solution.html')
#-----------------------------------------------------------------------------------------------------------
def aboutpage(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        return render(request, 'thankyou.html')
    return render(request,'contact.html')
#------------------------------------------------------
def download(request):
    try:
        wrapper = FileWrapper(open('log.pdf', 'rb'))
        response = HttpResponse(wrapper, content_type='application/force-download')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename('log.pdf')
        return response
    except Exception as e:
        return None
