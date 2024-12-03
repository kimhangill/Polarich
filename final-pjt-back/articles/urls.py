from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet,CommentViewSet


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)  # /articles/ 엔드포인트 생성
router.register(r'comments', CommentViewSet)

urlpatterns = [ 
    path('', include(router.urls))
    ]
#router url pattern