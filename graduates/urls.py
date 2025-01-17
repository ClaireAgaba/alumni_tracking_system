from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('graduates/', views.graduate_list, name='graduate_list'),
    path('graduates/add/', views.add_graduate, name='add_graduate'),
    path('graduates/upload/', views.upload_graduates, name='upload_graduates'),
    path('graduates/template/', views.download_excel_template, name='download_template'),
    path('graduates/export/excel/', views.export_graduates_excel, name='export_excel'),
    path('graduates/export/pdf/', views.export_graduates_pdf, name='export_pdf'),
    path('graduates/edit/<int:pk>/', views.edit_graduate, name='edit_graduate'),
    path('api/exam-centers/', views.get_exam_centers, name='get_exam_centers'),
    path('api/programs/', views.get_programs, name='get_programs'),
    path('api/districts/', views.get_districts, name='get_districts'),
]
