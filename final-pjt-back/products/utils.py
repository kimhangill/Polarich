from django.db.models import Count
from .models import DepositProducts, SavingProducts
from datetime import date
from accounts.models import Portfolio
from django.contrib.auth import get_user_model

User=get_user_model()

# 사용자의 나이 계산
def get_age_group(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    # 나이대 계산
    if age < 20:
        return 'under_20'
    elif 20 <= age < 30:
        return '20s'
    elif 30 <= age < 40:
        return '30s'
    elif 40 <= age < 50:
        return '40s'
    elif 50 <= age < 60:
        return '50s'
    else:
        return '60_and_above'


#사람들이 많이 즐겨찾은 O
def get_popular_recommendations():
    popular_deposits = DepositProducts.objects.annotate(favorite_count=Count('deposit_favorite_users')).order_by('-favorite_count')[:9]
    popular_savings = SavingProducts.objects.annotate(favorite_count=Count('saving_favorite_users')).order_by('-favorite_count')[:9]
    return popular_deposits, popular_savings


# {{ 직업 }}들이 선호하는 O
def get_occupation_based_recommendations(username):
    try:
        # 사용자의 포트폴리오 가져오기
        user = User.objects.get(username=username)  # username을 통해 user를 가져옵니다.
        portfolio = user.portfolios.first()  # 첫 번째 포트폴리오 객체를 가져옵니다.
    except Portfolio.DoesNotExist or User.DoesNotExist:
        print(username)
        # 포트폴리오가 없는 경우 None 반환
        return None, None
    same_occupation_users = User.objects.filter(portfolios__occupation=portfolio.occupation).exclude(id=user.id).prefetch_related('savings', 'deposits')
    # 예금 및 적금 상품 필터링
    recommended_deposits = DepositProducts.objects.filter(deposit_favorite_users__in=same_occupation_users).annotate(
        favorite_count=Count('deposit_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    recommended_savings = SavingProducts.objects.filter(saving_favorite_users__in=same_occupation_users).annotate(
        favorite_count=Count('saving_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    return recommended_deposits, recommended_savings

#회원님의 {{goal}} 목표를 위해
def get_financial_goal_based_recommendations(username):
    try:
        # 사용자의 포트폴리오 가져오기
        user = User.objects.get(username=username)  # username을 통해 user를 가져옵니다.
        portfolio = user.portfolios.first()  # 첫 번째 포트폴리오 객체를 가져옵니다.
    except Portfolio.DoesNotExist:
        # 포트폴리오가 없는 경우 None 반환
        return None, None
    
    same_financial_goal_users = User.objects.filter(portfolios__financial_goal=portfolio.financial_goal).exclude(id=user.id).prefetch_related('savings', 'deposits')
    # 예금 및 적금 상품 필터링
    recommended_deposits = DepositProducts.objects.filter(deposit_favorite_users__in=same_financial_goal_users).annotate(
        favorite_count=Count('deposit_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    recommended_savings = SavingProducts.objects.filter(saving_favorite_users__in=same_financial_goal_users).annotate(
        favorite_count=Count('saving_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    return recommended_deposits, recommended_savings

# {{age}}대 {{gender}}들이 많이 찾는
def get_recommendations_by_age_gender(username):
    try:
        # 사용자의 포트폴리오 및 추가 정보 가져오기
        user = User.objects.get(username=username)
        # 나이대 및 성별 가져오기
        if not user.date_of_birth or not user.gender:
            # 생년월일 또는 성별 정보가 없을 경우 None 반환
            return None, None
        age_group = get_age_group(user.date_of_birth)
        gender = user.gender
        # 같은 나이대 및 성별 사용자 필터링
        filtered_users = User.objects.filter(date_of_birth__isnull=False,gender=gender).exclude(id=user.id)# 같은 나이대 필터링 (계산된 나이대를 이용해 필터링)
        filtered_users = [u for u in filtered_users if get_age_group(u.date_of_birth) == age_group]

    except User.DoesNotExist:
        # 유저가 없는 경우 None 반환
        return None, None

    # 예금 및 적금 상품 필터링
    recommended_deposits = DepositProducts.objects.filter(deposit_favorite_users__in=filtered_users).annotate(
        favorite_count=Count('deposit_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    recommended_savings = SavingProducts.objects.filter(saving_favorite_users__in=filtered_users).annotate(
        favorite_count=Count('saving_favorite_users')
    ).order_by('-favorite_count').distinct()[:9]

    return recommended_deposits, recommended_savings