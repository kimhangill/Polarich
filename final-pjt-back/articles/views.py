from django.shortcuts import render
from rest_framework import permissions, viewsets,filters
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
from .models import Article,Comment
from django.db import models
from .serializers import ArticleListSerializer, ArticleSerializer,ArticleImage, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes, action
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .utils import get_finance_answer
from django.conf import settings

#viewset 기능 활용 테스트!
class ArticleViewSet(viewsets.ModelViewSet):
    filter_backends=[filters.SearchFilter]
    search_fields=['title','content','user__nickname']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Article.objects.all().order_by('-id') 
    parser_classes = (MultiPartParser, FormParser) 
    def get_queryset(self):
        queryset = Article.objects.all().order_by('-id')  # id 기준으로 오름차순 정렬
        article_type = self.request.query_params.get('type', None)
        if article_type:
            queryset = queryset.filter(type=article_type)
        return queryset
    
    
    
    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        article = self.get_object()  # 해당 게시글 객체 가져오기
        comments = article.comments.all().order_by('-id')  # 게시글의 모든 댓글 가져오기
        serializer = CommentSerializer(comments, many=True)  # 댓글 리스트 직렬화
        return Response(serializer.data)

    
    #검색 추가 조정 필요, 혹시 시간 없으면 그냥 통합검색으로 퉁칠 예정.
    def get_search_fields(self, view, request):
        search_type = request.query_params.get('search_type', 'title_content')
        if search_type == 'title_content':
            return ['title', 'content']
        elif search_type == 'nickname':
            return ['user__nickname']
        return []
    
    
    def get_serializer_class(self): #get일 경우 ArticleList 시리얼라이저 반환, 나머지일 경우 Article시리얼라이저 반환
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer
    
    def perform_create(self, serializer):
        article= serializer.save(user=self.request.user)
        images = self.request.FILES.getlist('images')  # 다수의 이미지 파일 가져오기
        for image in images:
            ArticleImage.objects.create(article=article, image=image)
            
        if article.type == 'qna':
            prompt = f"질문 제목:{article.title}\n질문 내용: {article.content}"
            answer = get_finance_answer(prompt)
        
            User=get_user_model()
            system_user = User.objects.get_or_create(id=settings.SYSTEM_USER_ID, is_superuser=False)[0]
        
        # 댓글 저장
            Comment.objects.create(
                article=article,
                user=system_user,
                content=answer
            )
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 제목 및 내용 업데이트
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 기존 이미지 처리 (필요 시)
        existing_images = request.data.getlist('existing_images', [])
        instance.images.exclude(id__in=existing_images).delete()

        # 새 이미지 저장
        new_images = request.FILES.getlist('new_images')
        for image in new_images:
            ArticleImage.objects.create(article=instance, image=image)

        return Response(serializer.data)
    
#코멘트 crud
class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user=self.request.user
        article = serializer.validated_data['article']
        user = self.request.user
        if article.type == 'qna' and not user.isProfessional:
            raise PermissionDenied("Q&A 답변에는 프로페셔널 권한이 필요합니다.")
        serializer.save(user=user)


