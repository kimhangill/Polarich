from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, TokenSerializer, TokenModel, UserDetailsSerializer
from allauth.account.adapter import get_adapter
from .models import User, Portfolio
from django.contrib.auth import get_user_model
from .utils import generate_nickname
from articles.serializers import ArticleListSerializer, CommentSerializer

User = get_user_model()

#회원가입 
class CustomRegisterSerializer(RegisterSerializer):
    
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    profileImage = serializers.ImageField(required=False, allow_null=True, use_url=True)
    nickname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_null=True)   
    def save(self, request):
        print('self.validated_data:', self.validated_data)
        print('self.cleaned_data:', self.get_cleaned_data)
        # 기본 사용자 정보를 먼저 저장
        user = super().save(request)
        # 추가 필드를 저장
        print(self.validated_data)

        user.date_of_birth = self.validated_data.get('date_of_birth', None)
        user.profileImage = self.validated_data.get('profileImage', None)
        user.nickname = self.validated_data.get('nickname', None)
        user.gender = self.validated_data.get('gender', None)
        user.save()  # 변경된 필드를 저장합니다.
        return user
    


#상세 회원정보 


# class PortFolioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Portfolio
#         read_only_fields = ('user',)

#포트폴리오 시리얼라이저
class PortfolioSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(source='user.date_of_birth', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)
    savings = serializers.StringRelatedField(source='user.savings', many=True, read_only=True)
    deposits = serializers.StringRelatedField(source='user.deposits', many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            'user', 'date_of_birth', 'gender', 'savings', 'deposits',
            'salary_range', 'occupation', 'investment_risk_profile',
            'financial_goal', 'experience_years', 'preferred_investment_period',
            'liquidity_preference', 'risk_tolerance', 'monthly_savings',
            'debt_ratio', 'preferred_investment_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'date_of_birth', 'gender', 'savings', 'deposits')

class CustomTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')
    username = serializers.CharField()


    class Meta:
        model = get_user_model()
        fields = ('token', 'username',)

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    profileImage = serializers.ImageField(required=False, allow_null=True)
    nickname = serializers.CharField(max_length=50)
    gender = serializers.CharField(required=False, allow_null=True)
    portfolio = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'date_of_birth', 'profileImage', 'nickname', 'gender', 'savings', 'deposits', 'isProfessional', 'portfolio','articles','comments']
        read_only_fields = ('username', 'id', 'date_of_birth', 'gender','comments','articles')

    def get_portfolio(self, obj):
        try:
            portfolio = Portfolio.objects.get(user=obj)
            return PortfolioSerializer(portfolio).data  # 포트폴리오 정보를 직렬화하여 반환
        except Portfolio.DoesNotExist:
            return None
        
    def get_articles(self, obj):
        articles = obj.article_set.all().order_by('-id')  # 해당 유저가 작성한 글
        return ArticleListSerializer(articles, many=True).data

    def get_comments(self, obj):
        comments = obj.comment_set.all().order_by('-id')  # 해당 유저가 작성한 댓글
        return CommentSerializer(comments, many=True).data