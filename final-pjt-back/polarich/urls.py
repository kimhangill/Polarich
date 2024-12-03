from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomRegisterView, CustomLoginView
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view()),
    path('', include('dj_rest_auth.urls')),
    # 기존의 dj_rest_auth.registration.urls를 삭제하고 커스텀 뷰 연결
    path('accounts/signup/', CustomRegisterView.as_view()),
    path('accounts/', include('allauth.urls')),
    # API 관련 엔드포인트들
    path('api/v1/', include('articles.urls')),     # articles 관련 URL 패턴
    path('api/v1/products/', include('products.urls')),     # products 관련 URL 패턴
    path('api/v1/accounts/', include('accounts.urls')),     # accounts 관련 URL 패턴
    path('api/v1/exchange/', include('exchange.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    # path('auth/social/', include('allauth.socialaccount.urls')), 소셜로그인 : 추후 구현 예정임.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   