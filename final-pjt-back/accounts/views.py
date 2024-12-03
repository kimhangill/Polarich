from dj_rest_auth.registration.views import RegisterView, LoginView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer, PortfolioSerializer, CustomTokenSerializer
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Portfolio
from articles.serializers import ArticleListSerializer, CommentSerializer
from products.models import SavingOptions, SavingProducts, DepositOptions, DepositProducts

class CustomLoginView(LoginView):
    def get_response(self):

        serializer_class = CustomTokenSerializer
        serializer = serializer_class(
            instance=self.user,  # self.token이 아닌 self.user를 전달
            context=self.get_serializer_context()
        )
        
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
# Create your views here.


#아이디 중복 체크 
#포스트맨 동작 확인.
@api_view(['GET'])
def check_duplicated(request):
    User = get_user_model()
    check_type = request.GET.get('type')
    value = request.GET.get('value')
    if not check_type or not value:
            return Response({"error": "type and value are required"}, status=status.HTTP_400_BAD_REQUEST)
    if check_type =='username':
        is_duplicated = User.objects.filter(username=value).exists()
    elif check_type == 'nickname':
        is_duplicated = User.objects.filter(nickname=value).exists()
    else:
        return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'is_duplicated':is_duplicated}, status=status.HTTP_200_OK)

#프로필 관리 기능(열람, 수정)
#포스트맨 동작 확인.
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request,username):
    if not request.user.is_authenticated:
        return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    # if request.user.username != username:
    #     return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)
    user=get_object_or_404(get_user_model(),username=username)
    if request.method =='GET':
        serializer=CustomUserDetailsSerializer(user)
        return Response(serializer.data)
    
    elif request.method =='PUT':
        serializer=CustomUserDetailsSerializer(instance=user,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_articles(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if not request.user.is_authenticated:
        return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user.username != username:
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)
    
    # 사용자 작성 글 가져오기
    articles = user.article_set.all().order_by('-id')
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_comments(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if not request.user.is_authenticated:
        return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user.username != username:
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)
    
    # 사용자 작성 댓글 가져오기
    comments = user.comment_set.all().order_by('-id')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


    
#계정 삭제 기능
#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request, username):
    #본인이 아니라면 에러 출력
    user=get_object_or_404(get_user_model(),username=username)
    
    if request.user != user:
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def portfolio(request,username):
    user=get_object_or_404(get_user_model(),username=username)
    
    if request.user != user:
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        if Portfolio.objects.filter(user=request.user).exists():
            return Response({'message':'이미 포트폴리오가 존재하는 유저입니다!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
    elif request.method == 'PUT':
        portfolio = get_object_or_404(Portfolio, user=user)
        serializer = PortfolioSerializer(instance=portfolio, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_portfolio(request, username):
    user=get_object_or_404(get_user_model(),username=username)
    if request.user != user:
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_403_FORBIDDEN)
    portfolio = Portfolio.objects.get(user=user)
    serializer = PortfolioSerializer(portfolio)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
        
from products.serializers import DepositProductListSerializer, SavingProductListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cal_avg(request):
    # 전체 유저 데이터
    all_saving_objects = SavingProducts.objects.filter(
        saving_favorite_users__isnull=False
    ).prefetch_related('options')
    all_deposit_objects = DepositProducts.objects.filter(
        deposit_favorite_users__isnull=False
    ).prefetch_related('options')

    saving_serializer = SavingProductListSerializer(
        all_saving_objects, many=True
    )
    deposit_serializer = DepositProductListSerializer(
        all_deposit_objects, many=True
    )

    # 요청 유저 데이터
    my_saving_objects = SavingProducts.objects.filter(
        saving_favorite_users=request.user
    ).prefetch_related('options')
    my_deposit_objects = DepositProducts.objects.filter(
        deposit_favorite_users=request.user
    ).prefetch_related('options')

    my_saving_serializer = SavingProductListSerializer(
        my_saving_objects, many=True
    )
    my_deposit_serializer = DepositProductListSerializer(
        my_deposit_objects, many=True
    )

    # 평균 금리 계산 함수
    def calculate_avg(products):
        intr_rates = [
            option['intr_rate']
            for product in products
            for option in product.get('options', [])
            if option.get('intr_rate', 0) > 0
        ]
        return round(sum(intr_rates) / len(intr_rates), 2) if intr_rates else 0

    # 전체 유저 평균 금리
    avg_deposit = calculate_avg(deposit_serializer.data)
    avg_saving = calculate_avg(saving_serializer.data)

    # 요청 유저 평균 금리
    my_avg_deposit = calculate_avg(my_deposit_serializer.data)
    my_avg_saving = calculate_avg(my_saving_serializer.data)

    # JSON 응답 반환
    return Response({
        'avg_deposit': avg_deposit,
        'avg_saving': avg_saving,
        'my_avg_deposit': my_avg_deposit,
        'my_avg_saving': my_avg_saving,
    })