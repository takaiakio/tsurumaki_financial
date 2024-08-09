from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),  # 'upload_csv'ビューに対応するURL
    path('analyze/<int:pk>/', views.analyze, name='analyze'),  # 'analyze'ビューに対応するURL
]

