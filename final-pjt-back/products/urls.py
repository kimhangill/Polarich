from django.urls import path
from . import views
from .views import RecommendationsView
urlpatterns = [
    #관리자만 입장 가능_상품 갱신
    path('secure/save_deposits/',views.save_deposit_products),
    path('secure/save_savings/',views.save_saving_products),
    path('secure/save_loans/',views.save_loan_products),
    #리스트 출력용
    path('deposits/', views.deposit_products),
    path('savings/',views.saving_products),
    #디테일 출력용
    path('deposits/<int:product_id>/', views.deposit_detail),
    path('savings/<int:product_id>/',views.saving_detail),
    #즐겨찾기 추가, 관리
    path('add_favorite/', views.add_favorite),
    path('favorites/',views.user_favorites),
    #즐겨찾기
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    #대출상품 확인용
    path('loans/',views.loan_products),
    #디테일 출력용
    path('loans/<int:product_id>/', views.loan_detail),
    
    #국토교통부 api 연동 후 지가 반환
    path('checkhouse/', views.check_house)
]
