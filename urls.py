from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
               path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),	      
               path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
	       path("UserLogin.html", views.UserLogin, name="UserLogin"),	      
               path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
               path("RegisterAction", views.RegisterAction, name="RegisterAction"),
               path("Register.html", views.Register, name="Register"),
               path("UploadMusic.html", views.UploadMusic, name="UploadMusic"),	      
               path("UploadMusicAction", views.UploadMusicAction, name="UploadMusicAction"),
	       path("ViewUser", views.ViewUser, name="ViewUser"),
	       path("Chatbot.html", views.Chatbot, name="Chatbot"),	
	       path("ChatData", views.ChatData, name="ChatData"),
	       path("MusicPlay", views.MusicPlay, name="MusicPlay"),
	       path("Stop", views.Stop, name="Stop"),
]
