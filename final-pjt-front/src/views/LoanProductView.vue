<template>
  <v-card width="60%" class="mx-auto">
    <!-- 다이얼로그 제목 -->
    <v-card-title class="section-title">
      {{ productDetail?.fin_prdt_nm }}
        
    </v-card-title>

    <!-- 제품 헤더 정보 -->
    <v-row class="product-header">
      <v-col cols="8">
        <div class="info-row">
          <v-icon color="#003366" class="mr-2" size="48">mdi-barcode</v-icon>
          <v-typography variant="h6" class="title">상품 코드:</v-typography>
          <v-typography variant="h6" class="value">{{ productDetail?.fin_prdt_cd }}</v-typography>
        </div>
        <div class="info-row">
          <v-icon color="#003366" class="mr-2" size="48">mdi-bank</v-icon>
          <v-typography variant="h6" class="title">금융사:</v-typography>
          <v-typography variant="h6" class="value">{{ productDetail?.kor_co_nm }}</v-typography>
    
        </div>
        <div class="info-row">
          <v-icon color="#003366" class="mr-2" size="48">mdi-account-cash</v-icon>
          <v-typography variant="h6" class="title">상품 유형:</v-typography>
          <v-typography variant="h6" class="value">{{ productDetail?.crdt_prdt_type_nm }}</v-typography>
        </div>
      </v-col>
      <v-col cols="3" class="text-right">
        <img :src="`../src/assets/bank/${productDetail?.kor_co_nm}.png`" alt="금융사 로고" class="bank-icon" width="200px"></img>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <!-- 추가 제품 정보 -->
    <v-row>
      <v-col cols="12">
        <div class="info-row">
          <v-icon color="#003366" class="mr-2" size="24">mdi-sign-direction</v-icon>
          <v-typography variant="h6" class="title">가입 방법</v-typography>
          <v-spacer></v-spacer>
          <v-typography variant="h6" class="value">{{ productDetail?.join_way }}</v-typography>
        </div>
      </v-col>
    </v-row>

    <v-divider></v-divider>
    <!-- 세부 옵션 섹션 -->
    <v-card-text>
      <v-typography variant="h5" class="details-title"><strong>세부 옵션</strong></v-typography>
      <div v-for="opt in productDetail.options" :key="opt.id" class="option-card">
        <v-divider class="option-divider"></v-divider>
        <v-card outlined>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2" size="24">mdi-percent</v-icon>
                  <v-typography variant="h6" class="title">금리 유형</v-typography>
                  <v-spacer></v-spacer>
                  <v-typography variant="h6" class="value">{{ opt.crdt_lend_rate_type_nm }}</v-typography>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2" size="24">mdi-currency-usd</v-icon>
                  <v-typography variant="h6" class="title">평균 금리</v-typography>
                  <v-spacer></v-spacer>
                  <v-typography variant="h6" class="value">{{ opt.crdt_grad_avg }}%</v-typography>
                </div>
              </v-col>
              <!-- 등급별 금리 정보 -->
              <v-col cols="12">
                <v-typography variant="h6" class="title mb-4">등급별 금리</v-typography>
                <v-row>
                  <v-col 
                    cols="12" 
                    sm="6" 
                    md="4" 
                    v-for="grade in loanGrades" 
                    :key="grade"
                  >
                    <v-card class="grade-card pa-4" v-if="opt[`crdt_grad_${grade}`]">
                      <v-row align="center">
                        <v-icon color="#003366" class="mr-2" size="24">mdi-grade</v-icon>
                      </v-row>
                      <v-typography variant="h5" class="grade-rate mt-2" color="#FF5722">
                        {{ grade }}등급: {{ opt[`crdt_grad_${grade}`] }}%
                      </v-typography>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </v-card-text>

    <!-- 돌아가기 버튼 -->
    <v-row class="text-center mt-4">
      <v-col>
        <v-btn color="primary" @click="goBack">돌아가기</v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import { useDepositStore, useLoanStore, useSavingStore } from '@/stores/productStores';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const productDetail = ref({});
let store;

if (route.params.type === 'saving') {
store = useSavingStore();
} else if (route.params.type === 'deposit') {
store = useDepositStore();
} else {
store = useLoanStore();
}

const isFavorite = ref(false);

onMounted(async () => {
productDetail.value = await store.fetchProductDetail(route.params.id);
// 초기 즐겨찾기 여부 확인
console.log(productDetail.value);

});

const toggleFavorite = async () => {
await store.addFavorite(productDetail.value.id);
isFavorite.value = !isFavorite.value;
};

const goBack = () => {
router.back()}

// 등급 목록 정의
const loanGrades = [1, 4, 5, 6, 10, 11, 12, 13];
</script>

<style scoped>
.dialog-title {
font-size: 2rem;
font-weight: bold;
color: #003366;
border-bottom: 1px solid #f5c242;
padding-bottom: 0.5rem;
}

.product-header {
padding: 1rem 0;
}

.info-row {
display: flex;
align-items: center;
margin-bottom: 0.75rem;
}

.title {
font-size: 1.2rem;
font-weight: 500;
}

.value {
font-size: 1.2rem;
color: #555;
}

.info-box {
margin-bottom: 1rem;
}

.text-box {
padding: 1rem;
background-color: #f9f9f9;
border: 1px solid #e0e0e0;
border-radius: 8px;
}

.info-box .v-card-text {
font-size: 1rem;
line-height: 1.5;
color: #333;
white-space: pre-wrap;
}

.details-title {
margin: 1.5rem 0 1rem;
color: #003366;
}

.option-card {
margin-bottom: 1rem;
}

.option-divider {
margin: 0;
}

.favorite-active {
background-color: #001f3f;
color: #FFD700;
transition: all 0.3s ease;
}

.favorite-inactive {
color: #808080;
transition: all 0.3s ease;
}

.grade-card {
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.3s;
}
.grade-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
.grade-title {
  font-weight: 600;
  color: #003366;
}
.grade-rate {
  font-weight: bold;
}



@media (max-width: 600px) {
.title,
.value {
  font-size: 1rem;
}

.dialog-title {
  font-size: 1.5rem;
}
}


</style>
