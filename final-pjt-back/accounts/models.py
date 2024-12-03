from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import generate_nickname
from products.models import SavingProducts,DepositProducts
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    isProfessional = models.BooleanField(default=False)
    date_of_birth=models.DateField(null=True, blank=True)
    profileImage = models.ImageField(upload_to='profile_images/',blank=True,null=True,
    default='images/default_profile.jpg')
    nickname = models.CharField(max_length=50, unique=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),       # 남성
        ('female', 'Female'),   # 여성
        ('other', 'Other'),     # 기타
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    savings= models.ManyToManyField(SavingProducts, related_name='saving_favorite_users')
    deposits= models.ManyToManyField(DepositProducts, related_name='deposit_favorite_users')

    def save(self, *args, **kwargs):
        if not self.nickname:  # 닉네임이 없을 경우 생성
            self.nickname = generate_nickname()
        super().save(*args, **kwargs)
    pass

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')

    # 기본 재정 정보
    SALARY_RANGE_CHOICES = [
        ('below_24m', 'below_24m'),           
        ('24m_to_36m', '24m_to_36m'),          
        ('36m_to_50m', '36m_to_50m'),          
        ('50m_to_70m', '50m_to_70m'),        
        ('70m_to_100m', '70m_to_100m'),      
        ('above_100m', 'above_100m'),         
    ]
    salary_range = models.CharField(max_length=20, choices=SALARY_RANGE_CHOICES, null=True, blank=True)  # 연봉 범위

    OCCUPATION_CHOICES = [
        ('student', 'student'), 
        ('employee', 'employee'),
        ('self_employed', 'self_employed'),
        ('retired', 'retired'),
        ('other', 'other'),
    ]
    occupation = models.CharField(max_length=50, choices=OCCUPATION_CHOICES, null=True, blank=True)  # 직업

    # 투자 성향
    INVESTMENT_RISK_CHOICES = [
        ('conservative', 'conservative'),  
        ('moderate', 'moderate'),          
        ('aggressive', 'aggressive'),      
    ]
    investment_risk_profile = models.CharField(max_length=50, choices=INVESTMENT_RISK_CHOICES, null=True, blank=True)  # 투자 성향

    FINANCIAL_GOAL_CHOICES = [
        ('home', 'home'),
        ('retirement', 'retirement'),
        ('education', 'education'),
        ('travel', 'travel'),
        ('investment', 'investment'),
    ]
    financial_goal = models.CharField(max_length=100, choices=FINANCIAL_GOAL_CHOICES, null=True, blank=True)  # 재무 목표

    EXPERIENCE_YEARS_CHOICES = [
        ('none', 'none'),
        ('less_than_1', 'less_than_1'),
        ('1_to_3', '1_to_3'),
        ('3_to_5', '3_to_5'),
        ('more_than_5', 'more_than_5'),
    ]
    experience_years = models.CharField(max_length=20, choices=EXPERIENCE_YEARS_CHOICES, null=True, blank=True)  # 투자 경험

    INVESTMENT_PERIOD_CHOICES = [
        ('short', 'short'),
        ('medium', 'medium'),
        ('long', 'long'),
    ]
    preferred_investment_period = models.CharField(max_length=50, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)  # 투자 기간

    LIQUIDITY_PREFERENCE_CHOICES = [
        ('high', 'high'),
        ('low', 'low'),
    ]
    liquidity_preference = models.CharField(max_length=20, choices=LIQUIDITY_PREFERENCE_CHOICES, null=True, blank=True)  # 유동성 선호 여부

    RISK_TOLERANCE_CHOICES = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    ]
    risk_tolerance = models.CharField(max_length=10,choices=RISK_TOLERANCE_CHOICES, null=True, blank=True)  # 위험 수용도

    MONTHLY_SAVINGS_CHOICES = [
        ('below_300', 'below_300'),
        ('300_to_500', '300_to_500'),
        ('500_to_1000', '500_to_1000'),
        ('1000_to_2000', '1000_to_2000'),
        ('above_2000', 'above_2000'),
    ]
    monthly_savings = models.CharField(max_length=20, choices=MONTHLY_SAVINGS_CHOICES, null=True, blank=True)  # 월 저축액

    DEBT_RATIO_CHOICES = [
        ('below_10', 'below_10'),
        ('10_to_30', '10_to_30'),
        ('30_to_50', '30_to_50'),
        ('50_to_70', '50_to_70'),
        ('above_70', 'above_70'),
    ]
    debt_ratio = models.CharField(max_length=20, choices=DEBT_RATIO_CHOICES, null=True, blank=True)  # 부채 비율

    PREFERRED_INVESTMENT_TYPE_CHOICES = [
        ('stocks', 'stocks'),
        ('real_estate', 'real_estate'),
        ('funds', 'funds'),
        ('bonds', 'bonds'),
        ('cryptocurrency', 'cryptocurrency'),
    ]
    preferred_investment_type = models.CharField(max_length=100, choices=PREFERRED_INVESTMENT_TYPE_CHOICES, null=True, blank=True)  # 선호하는 투자 유형

    created_at = models.DateTimeField(auto_now_add=True)  # 포트폴리오 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)      # 포트폴리오 업데이트 날짜

    def __str__(self):
        return f"{self.user.nickname}님의 투자 정보입니다!"
