from django.urls import path
from . import views


urlpatterns = [
    path('check_duplicated/', views.check_duplicated),
    path('profiles/<str:username>/', views.user_profile),
    path('profile/<str:username>/articles/', views.user_articles),
    path('profile/<str:username>/comments/', views.user_comments),
    path('profiles/<str:username>/portfolio/', views.user_portfolio),
    path('delete/<str:username>/', views.user_delete),
    path('portfolio/<str:username>/', views.portfolio),
    path('avg/', views.cal_avg),
]
