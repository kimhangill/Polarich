from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status
import requests
from .models import DepositOptions, DepositProducts,SavingProducts,SavingOptions, creditLoanProducts,creditLoanOptions
from .serializers import CreditLoanOptionSerializer, DepositOptionsSerializer, DepositProductsSerializer, SavingProductsSerializer, SavingOptionsSerializer, UserFavoritesSerializer,FavoriteSerializer, SavingProductListSerializer, DepositProductListSerializer, CreditLoanProductDetailSerializer, CreditLoanProductListSerializer
from rest_framework.response import Response
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Max
from .utils import get_popular_recommendations, get_occupation_based_recommendations, get_financial_goal_based_recommendations, get_recommendations_by_age_gender
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


API_KEY = settings.API_KEY_DEPOSIT
API_KEY_HOUSE=settings.API_KEY_HOUSE

paginator = PageNumberPagination()
paginator.page_size = 25  # 페이지 크기
#예 적금 api 호출 후 db 저장 함수
@api_view(['GET'])
def save_deposit_products(request):
    cnt=0
    for page in range(1,10):
        FINLIFE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

        params={
            'auth':API_KEY,
            'TopFinGrpNo': '020000',
            'pageNo': page,
        }

        response = requests.get(url=FINLIFE_URL, params=params).json()
        products = response.get('result').get("baseList")
        options=response.get('result').get('optionList')
        for product in products:
            fin_prdt_cd= product.get('fin_prdt_cd')
            save_product={
                'fin_prdt_cd':fin_prdt_cd,
                'kor_co_nm':product.get('kor_co_nm'),
                'fin_prdt_nm':product.get('fin_prdt_nm'),
                'etc_note':product.get('etc_note'),
                'join_deny':product.get('join_deny'),
                'join_member':product.get('join_member'),
                'join_way':product.get('join_way'),
                'spcl_cnd':product.get('spcl_cnd'),
            }

            if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                continue


            serializer=DepositProductsSerializer(data=save_product)
            if serializer.is_valid():
                cnt+=1
                serializer.save()

        for option in options:
            fin_prdt_cd=option.get('fin_prdt_cd')
            save_trm=option.get('save_trm')

            if DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm).exists():
                continue
            origin_product=DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            if origin_product:
                save_option={
                    'fin_prdt_cd':option.get('fin_prdt_cd'),
                    'intr_rate_type_nm':option.get('intr_rate_type_nm'),
                    'intr_rate':option.get('intr_rate') or -1,
                    'intr_rate2':option.get('intr_rate2') or -1 ,
                    'save_trm':save_trm
                }
                serializer=DepositOptionsSerializer(data=save_option)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=origin_product)
    return Response({'save':f'성공적으로 {cnt}개 저장되었습니다.'})

@api_view(['GET'])
def save_saving_products(request):
    FINLIFE_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

    params={
        'auth':API_KEY,
        'TopFinGrpNo': '020000',
        'pageNo': 1,
    }

    response = requests.get(url=FINLIFE_URL, params=params).json()
    products = response.get('result').get("baseList")
    options=response.get('result').get('optionList')
    for product in products:
        fin_prdt_cd= product.get('fin_prdt_cd')
        save_product={
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':product.get('kor_co_nm'),
            'fin_prdt_nm':product.get('fin_prdt_nm'),
            'etc_note':product.get('etc_note'),
            'join_deny':product.get('join_deny'),
            'join_member':product.get('join_member'),
            'join_way':product.get('join_way'),
            'spcl_cnd':product.get('spcl_cnd'),
        }

        if SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue


        serializer=SavingProductsSerializer(data=save_product)
        if serializer.is_valid():
            serializer.save()

    for option in options:
        fin_prdt_cd=option.get('fin_prdt_cd')
        save_trm=option.get('save_trm')

        if SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm).exists():
            continue


        origin_product=SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

        save_option={
            'fin_prdt_cd':option.get('fin_prdt_cd'),
            'intr_rate_type_nm':option.get('intr_rate_type_nm'),
            'intr_rate':option.get('intr_rate') or -1,
            'intr_rate2':option.get('intr_rate2') or -1 ,
            'save_trm':save_trm
        }


        serializer=SavingOptionsSerializer(data=save_option)
        if serializer.is_valid():
            serializer.save(product=origin_product)

    return Response({'save':'성공적으로 저장되었습니다.'})
#예 적금 리스트 출력 함수.


@api_view(['GET','POST'])
def deposit_products(request):
    # 1. 검색 기능 구현    
    
    search_query = request.GET.get('search', '')  # 기본값은 빈 문자열
    if search_query!='':
        search_terms = search_query.split()  # 공백 기준으로 분리
        products = DepositProducts.objects.filter(
            Q(kor_co_nm__icontains=search_terms[0]) | Q(fin_prdt_nm__icontains=search_terms[0]))
    else:
        products = DepositProducts.objects.all()
    # 2. 정렬 기능 구현
    sort_key = request.GET.get('sort', '-id')  # 기본값은 최근 등록순
    save_trm = request.GET.get('save_trm', None)
    if sort_key == 'interest_rate' and save_trm:
        try:
            save_trm_value = int(save_trm)
            products = products.filter(options__save_trm=save_trm_value).order_by('-options__intr_rate')
        except ValueError:
            return Response({"error": "Invalid save_trm value. It should be an integer."}, status=400)
    else:
        products = products.order_by(sort_key)
        paginated_products = paginator.paginate_queryset(products, request)

    # 3. 직렬화 및 응답
    serializer = DepositProductListSerializer(paginated_products, many=True)
    print(serializer.data)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def saving_products(request):
    # 1. 검색 기능 구현
    search_query = request.GET.get('search', '')  # 기본값은 빈 문자열
    if search_query!='':
        search_terms = search_query.split()  # 공백 기준으로 분리
        products = SavingProducts.objects.filter(
            Q(kor_co_nm__icontains=search_terms[0]) | Q(fin_prdt_nm__icontains=search_terms[0]))
    else:
         products = SavingProducts.objects.all()
    # 2. 정렬 기능 구현
    sort_key = request.GET.get('sort', '-id')  # 기본값은 최근 등록순
    save_trm = request.GET.get('save_trm', None)
    if sort_key == 'interest_rate' and save_trm:
        try:
            save_trm_value = int(save_trm)
            products = products.filter(options__save_trm=save_trm_value).order_by('-options__intr_rate')
        except ValueError:
            return Response({"error": "Invalid save_trm value. It should be an integer."}, status=400)
    else:
        products = products.order_by(sort_key)
        paginated_products = paginator.paginate_queryset(products, request)
    # 3. 직렬화 및 응답
    serializer = SavingProductListSerializer(paginated_products, many=True)
    print("we deposit down saving.")
    print(serializer.data)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def deposit_detail(request, product_id):
    product = get_object_or_404(DepositProducts, pk=product_id)
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def saving_detail(request, product_id):
    product = get_object_or_404(SavingProducts, pk=product_id)
    serializer = SavingProductsSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

    #이 부분에 PUT으로 관리자만이 옵션 변경 시 수정할 수 있는 함수 필요
    #수정 후, email을 통해 해당 상품 보유자에게 메시지가 전달되어야 함.
#즐겨찾기 관련 기능
@api_view(['POST'])
def add_favorite(request):
    user = request.user
    # 1. 요청 데이터 검증을 위한 serializer 인스턴스 생성
    serializer = FavoriteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    # 2. 검증된 데이터 가져오기
    product_type = serializer.validated_data['product_type']
    product_id = serializer.validated_data['product_id']
    # 3. 상품 아이디에 맞는 상품 선택
    if product_type == 'savings':
        product = get_object_or_404(SavingProducts, pk=product_id)
        if product in user.savings.all():
            # 즐겨찾기 해제 로직
            user.savings.remove(product)
            message = "적금 상품 즐겨찾기가 해제되었습니다."
        else:
            # 즐겨찾기 추가 로직
            user.savings.add(product)
            message = "적금 상품이 즐겨찾기에 추가되었습니다."
    elif product_type == 'deposits':
        product = get_object_or_404(DepositProducts, pk=product_id)
        if product in user.deposits.all():
            # 즐겨찾기 해제 로직
            user.deposits.remove(product)
            message = "예금 상품 즐겨찾기가 해제되었습니다."
        else:
            # 즐겨찾기 추가 로직
            user.deposits.add(product)
            message = "예금 상품이 즐겨찾기에 추가되었습니다."
    # 4. 응답 반환
    return Response({"message": message}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    print(request.data)
    print(request.auth)
    user = request.user  # 현재 로그인된 유저
    # UserFavoritesSerializer를 사용하여 유저 인스턴스를 직렬화
    serializer = UserFavoritesSerializer(user)
    # 직렬화된 데이터를 JSON 응답으로 반환
    return Response(serializer.data)

#추천 알고리즘별 딕셔너리 + 상품추천 알고리즘
RECOMMENDATION_FUNCTIONS = {
    'popular': get_popular_recommendations,
    'occupation': get_occupation_based_recommendations,
    'financial_goal': get_financial_goal_based_recommendations,
    'age_gender': get_recommendations_by_age_gender,
}
RECOMMENDATION_FUNCTIONS = {
    'popular': get_popular_recommendations,
    'occupation': get_occupation_based_recommendations,
    'financial_goal': get_financial_goal_based_recommendations,
    'age_gender': get_recommendations_by_age_gender,
}

class RecommendationsView(APIView):
    def get(self, request):
        # 사용자의 username 가져오기
        username = request.user.username

        # 모든 추천 유형에 대해 결과를 담을 딕셔너리 초기화
        all_recommendations = {}

        # 각 추천 유형에 대한 함수 호출
        for recommendation_type, recommendation_function in RECOMMENDATION_FUNCTIONS.items():
            # 추천 함수 호출
            if recommendation_type == 'popular':
                deposits, savings = recommendation_function()
            else:
                deposits, savings = recommendation_function(username)

            # 추천 결과 유효성 확인
            if deposits is None or savings is None:
                return Response({"error": f"{recommendation_type} 유형의 추천을 제공할 수 없습니다."}, status=400)

            # 직렬화된 추천 결과 저장
            deposit_serializer = DepositProductsSerializer(deposits, many=True)
            saving_serializer = SavingProductsSerializer(savings, many=True)

            # 각 추천 유형의 결과를 딕셔너리에 저장
            all_recommendations[recommendation_type] = {
                "recommended_deposits": deposit_serializer.data,
                "recommended_savings": saving_serializer.data
            }

        # 모든 추천 결과 응답
        return Response(all_recommendations)


#대출상품 조회, 저장

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loan_products(request):
    search_query = request.GET.get('search', '')  # 기본값은 빈 문자열
    products = creditLoanProducts.objects.filter(
        Q(kor_co_nm__icontains=search_query)|Q(fin_prdt_nm__icontains=search_query))
    # 평균 금리 기준 정렬
    sort_key = request.GET.get('sort', '-id')  # 기본값은 최근 등록순
    if sort_key == 'average_rate':
        products = products.order_by('-options__crdt_grad_avg')
    else:
        products = products.order_by(sort_key)
        paginated_products = paginator.paginate_queryset(products, request)
    # 3. 직렬화 및 응답
    serializer = CreditLoanProductListSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def loan_detail(request,product_id):
    product = get_object_or_404(creditLoanProducts, pk=product_id)
    serializer = CreditLoanProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def save_loan_products(request):
    type=['rentHouseLoanProducts','mortgageLoanProducts','creditLoanProducts']
    FINLIFE_URL = 'http://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json'

    params = {
        'auth': API_KEY,
        'TopFinGrpNo': '020000',
        'pageNo': 1,
    }

    response = requests.get(url=FINLIFE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        products = data.get('result', {}).get('baseList', [])
        options = data.get('result', {}).get('optionList', [])

        for product in products:
            if creditLoanProducts.objects.filter(fin_prdt_cd=product.get('fin_prdt_cd')).exists():
                continue
            serializer = CreditLoanProductDetailSerializer(data=product)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        for option in options:
            origin_product = creditLoanProducts.objects.filter(fin_prdt_cd=option.get('fin_prdt_cd')).first()
            if origin_product is None:
                continue
            if creditLoanOptions.objects.filter(product=origin_product, crdt_lend_rate_type=option.get('crdt_lend_rate_type')).exists():
                continue
            option['product'] = origin_product.id  # 외래키 필드 설정
            serializer = CreditLoanOptionSerializer(data=option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=origin_product)

        return Response({'message': '성공적으로 저장되었습니다.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': f'API 요청 실패: {response.status_code}'}, status=status.HTTP_400_BAD_REQUEST)
    


import requests
import json
import xmltodict

@api_view(['GET'])
def check_house(request):
    address = request.GET.get('address')
    dong = request.GET.get('dong')
    jibun = request.GET.get('jibun')
    type = 'Apt' if request.GET.get('type') == '아파트' else 'PH'
    API_KEY_HOUSE = settings.API_KEY_HOUSE

    result = []
    print(request.GET)
    for year in range(2022,2024):
        for mm in range(1, 13):
            if year==2024 and mm==12:
                continue
            month = f"{mm:02d}"  # 월을 두 자리 형식으로 변환
            if type=='Apt':
                url = f'https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?serviceKey={API_KEY_HOUSE}&LAWD_CD={address}&DEAL_YMD={year}{month}&pageNo=1&numOfRows=100'
            else:
                url = f'https://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade?LAWD_CD={address}&DEAL_YMD=2024{month}&serviceKey={API_KEY_HOUSE}'

            response = requests.get(url)
            if response.status_code == 200:
                try:
                    dict_data = xmltodict.parse(response.text)
                    json_data = json.loads(json.dumps(dict_data))  # 문자열 → 딕셔너리
                        # 데이터 추출 및 필터링
                    items = json_data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                    if items:
                        for item in items:
                            if item:
                                if item.get('jibun') == jibun:
                                    result.append({'price': item.get('dealAmount'), 'year':year,'month': mm})
                except KeyError as e:
                    return Response({'error': f'필요한 데이터가 없습니다: {e}'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    continue
            else:
                return Response({'error': f'외부 API 요청 실패: {response.status_code}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)
