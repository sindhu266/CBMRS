from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pickle
import pymysql
import os
from django.core.files.storage import FileSystemStorage
import multiprocessing
import winsound

global uname, playname

def trainModel(query):
    global vectorizer, tfidf
    answers = []
    details = []
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM music")
        rows = cur.fetchall()
        for row in rows:
            desc = row[2]
            for k in range(len(query)):
                print(query[k]+" == "+desc)
                if query[k] in desc and row[1] not in answers:
                    answers.append(row[1])
                    details.append([row[0], row[1], row[2]])
    return details

def play_audio():
    global playname
    winsound.PlaySound(playname, winsound.SND_FILENAME)

def stop_audio():
    winsound.PlaySound(None, winsound.SND_FILENAME)

def MusicPlay(request):
    if request.method == 'GET':
        global playname
        name = request.GET.get('t1', False)
        playname = "MusicApp/static/files/"+name
        #play = multiprocessing.Process(target=play_audio)
        #play.start()
        winsound.PlaySound(playname, winsound.SND_FILENAME)
        return HttpResponse("", content_type="text/plain")

def Stop(request):
    if request.method == 'GET':
        '''
        global play
        play = multiprocessing.Process(target=stop_audio)
        play.start()
        '''
        winsound.PlaySound(None, winsound.SND_FILENAME)
        return HttpResponse("", content_type="text/plain")

def Chatbot(request):
    if request.method == 'GET':
        return render(request, 'Chatbot.html', {})

def ChatData(request):
    if request.method == 'GET':
        question = request.GET.get('mytext', False)
        query = question
        query = query.lower()
        print(query)
        output = "Chatbot: Unable to predict answers. Please Try Again"
        if "about" in query or "who" in query or "describe" in query or "yourself" in query:
            output = "Chatbot: I am a music Chatbot who recommend Music to user based on their commands"
        elif "type" in query or "music" in query:
            output = "Chatbot: I have huge list of albums on various categories such as Sad, Joy, Romance etc."
        elif "long" in query or "work" in query:
            output = "Chatbot: I worked 24 X 7"
        elif "hello" in query or "hi" in query:
            output = "Chatbot: Hello"
        elif "how" in query or "are" in query:
            output = "Chatbot: I am Good."    
        else:
            result = trainModel(query.split(" "))
            if len(result) == 0:
                output = "Chatbot: Sorry! i am not trained to serve answer for this question. Please! Retry"
            else:
                output = ""
                for i in range(len(result)):
                    temp = result[i]
                    music = temp[0]
                    file = temp[1]
                    desc = temp[2]
                    link = file+','+desc
                    output += link+"#"
                output += "Stop,Stop Playing"   
        print(output)    
        return HttpResponse(output, content_type="text/plain")   

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})
    
def AdminLogin(request):
    if request.method == 'GET':
        return render(request, 'AdminLogin.html', {})    

def AdminLoginAction(request):
    if request.method == 'POST':
        global userid
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == "admin" and password == "admin":
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid Login'}
            return render(request, 'AdminLogin.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)


def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup Process Completed. You can Login now"
        context= {'data': status}
        return render(request, 'Register.html', context)

def UploadMusic(request):
    if request.method == 'GET':
       return render(request, 'UploadMusic.html', {})    

def UploadMusicAction(request):
    if request.method == 'POST':
        music = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        desc = desc.lower().strip()
        filename = request.FILES['t3'].name
        myfile = request.FILES['t3'].read()
        status = "Error in adding music details"
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO music(music_name, filename, description) VALUES('"+music+"','"+filename+"','"+desc+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            status = "Music details added to database"
            if os.path.exists("MusicApp/static/files/"+filename):
                os.remove("MusicApp/static/files/"+filename)
            with open("MusicApp/static/files/"+filename, "wb") as file:
                file.write(myfile)
            file.close()             
        context= {'data': status}
        return render(request, 'UploadMusic.html', context)

def ViewUser(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Password</th><th><font size="" color="black">Contact No</th>'
        output+='<th><font size="" color="black">Email ID</th><th><font size="" color="black">Address</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'ChatbotMusic',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from register")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+str(row[1])+'</td><td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td><td><font size="" color="black">'+row[4]+'</td></tr>'
        output+= "</table></br></br></br></br>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)    





    
