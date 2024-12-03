from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

# 예금 옵션 직렬화기
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = (
            'id',                # 옵션의 고유 ID
            'fin_prdt_cd',       # 금융상품 코드
            'intr_rate_type_nm', # 금리 유형
            'intr_rate',         # 기본 금리
            'intr_rate2',        # 우대 금리
            'save_trm',          # 저축 기간
            'product',           # 연결된 원본 상품 정보
        )
        read_only_fields=('product',)
# 적금 옵션 직렬화기
class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = (
            'id',                # 옵션의 고유 ID
            'fin_prdt_cd',       # 금융상품 코드
            'intr_rate_type_nm', # 금리 유형
            'intr_rate',         # 기본 금리
            'intr_rate2',        # 우대 금리
            'save_trm',          # 저축 기간
            'product',           # 연결된 원본 상품 정보
        )
        read_only_fields=('product',)
# 예적금 상품 리스트 직렬화기
class DepositProductListSerializer(serializers.ModelSerializer):
    class DepositOptionSummarySerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = ('save_trm', 'intr_rate')  # 기간과 기본 금리만 포함
            
    options = DepositOptionSummarySerializer(many=True, read_only=True)  # 옵션 요약 정보만 포함

    class Meta:
        model = DepositProducts
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'options')  # 요약 정보 필드만 포함

class SavingProductListSerializer(serializers.ModelSerializer):
    class SavingOptionSummarySerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingOptions
            fields = ('save_trm', 'intr_rate')  # 기간과 기본 금리만 포함
            
    options = SavingOptionSummarySerializer(many=True, read_only=True)  # 옵션 요약 정보만 포함

    class Meta:
        model = SavingProducts
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'options')  # 요약 정보 필드만 포함

class SavingProductsSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProducts
        fields = (
            'id',            # 상품의 고유 ID
            'fin_prdt_cd',   # 금융상품 코드
            'kor_co_nm',     # 금융사 이름
            'fin_prdt_nm',   # 상품 이름
            'etc_note',      # 기타 사항
            'join_deny',     # 가입 제한 여부
            'join_member',   # 가입 대상
            'join_way',      # 가입 방법
            'spcl_cnd',      # 특별 조건
            'options',
        )

class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProducts
        fields = (
            'id',            # 상품의 고유 ID
            'fin_prdt_cd',   # 금융상품 코드
            'kor_co_nm',     # 금융사 이름
            'fin_prdt_nm',   # 상품 이름
            'etc_note',      # 기타 사항
            'join_deny',     # 가입 제한 여부
            'join_member',   # 가입 대상
            'join_way',      # 가입 방법
            'spcl_cnd',      # 특별 조건
            'options',
        )
class UserFavoritesSerializer(serializers.ModelSerializer):
    deposits = SavingProductListSerializer(many=True, read_only=True)  # 예금 옵션 즐겨찾기 정보
    savings = SavingProductListSerializer(many=True, read_only=True)  # 적금 옵션 즐겨찾기 정보

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'savings', 'deposits']
class FavoriteSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=['savings', 'deposits'])
    product_id = serializers.IntegerField()
#신용대출 상품 목록 직렬화기
class CreditLoanProductListSerializer(serializers.ModelSerializer):
    average_rate = serializers.FloatField(source='options.crdt_grad_avg', read_only=True)

    class Meta:
        model = creditLoanProducts
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'crdt_prdt_type', 'crdt_prdt_type_nm', 'join_way', 'average_rate')

class CreditLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = creditLoanOptions
        fields = (
            'id',                  # 옵션의 고유 ID
            'crdt_lend_rate_type', # 금리 유형
            'crdt_lend_rate_type_nm',   # 금리 유형 이름
            'crdt_grad_1',         # 1등급 금리
            'crdt_grad_4',         # 4등급 금리
            'crdt_grad_5',         # 5등급 금리
            'crdt_grad_6',         # 6등급 금리
            'crdt_grad_10',        # 10등급 금리
            'crdt_grad_11',        # 11등급 금리
            'crdt_grad_12',        # 12등급 금리
            'crdt_grad_13',        # 13등급 금리
            'crdt_grad_avg',       # 평균 금리
            'product',
            )
        read_only_fields=('product',)
# 신용대출 상품 상세용 시리얼라이저
class CreditLoanProductDetailSerializer(serializers.ModelSerializer):

    options = CreditLoanOptionSerializer(many=True, read_only=True)
    class Meta:
        model = creditLoanProducts
        fields = (
            'id',                # 상품의 고유 ID
            'fin_prdt_cd',       # 금융상품 코드
            'kor_co_nm',         # 금융사 이름
            'fin_prdt_nm',       # 상품 이름
            'crdt_prdt_type',    # 신용대출 상품 유형
            'crdt_prdt_type_nm', # 신용대출 상품 유형 이름
            'join_way',          # 가입 방법
            'options',           # 연결된 옵션들
        )
