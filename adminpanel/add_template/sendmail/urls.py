from django.urls import path

from add_template.sendmail import views

urlpatterns = [
    path('add_template/', views.add_template.as_view()),
] 
