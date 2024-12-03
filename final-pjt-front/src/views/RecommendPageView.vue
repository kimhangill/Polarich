<template>
  <v-container>
    <!-- 큰 헤더 이미지 추가 -->
    <!-- 메인 타이틀 중앙 정렬 및 크기 증가 -->
    <h1 class="section-title">폴라리치의 추천 금융상품</h1>

    <!-- 상단 옵션 목록 -->
    <v-row>
      <v-col cols="12">
        <v-tabs v-model="selectedOption" align-tabs="start" :color="primary">
          <v-tab
            v-for="(option, index) in rightOptions"
            :key="index"
            :class="{ 'tab-selected': selectedOption === index }"
            @click="selectOption(index)"
            ripple
          >
            {{ option }}
          </v-tab>
        </v-tabs>
      </v-col>
    </v-row>

    <!-- 데이터 로딩 상태 -->
    <div v-if="isLoading" class="loading">
      데이터를 불러오는 중입니다...
    </div>

    <!-- 추천 상품 데이터 -->
    <template v-else>
      <!-- 예금 섹션 -->
      <h2 v-if="recommendedDeposits.length" class="section-title">
        추천 예금 상품
      </h2>
      <div v-else class="empty-message">
        아직 길잡이별이 충분히 빛나지 않았어요
      </div>

      <!-- 예금 섹션 카드 그리드 -->
      <v-row v-if="recommendedDeposits.length" class="card-grid"  align="stretch">
        <v-col cols="12" sm="6" md="4" lg="2" v-for="product in recommendedDeposits" :key="'deposit-product-' + product.id">
          <v-card class="clickable-card uniform-card" @click="navigateToPage(`/deposit/${product.id}`)">
            <img :src="`../src/assets/bank/${product.kor_co_nm}.png`" class="bank-logo" alt="bank" height="60px"/>
            <v-card-title class="truncate">
              {{ product.fin_prdt_nm }}
            </v-card-title>
            <v-card-subtitle class="truncate">{{ product.kor_co_nm }}</v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>

      <!-- 적금 섹션 -->
      <h2 v-if="recommendedSavings.length" class="section-title">
        추천 적금 상품
      </h2>
      <div v-else class="empty-message">
        아직 길잡이별이 충분히 빛나지 않았어요
      </div>

      <!-- 적금 섹션 카드 그리드 -->
      <v-row v-if="recommendedSavings.length" class="card-grid"  align="stretch">
        <v-col cols="12" sm="6" md="4" lg="2" v-for="product in recommendedSavings" :key="'saving-product-' + product.id"  class="d-flex">
          <v-card class="clickable-card uniform-card flex-grow-1" @click="navigateToPage(`/saving/${product.id}`)">
            <img :src="`../src/assets/bank/${product.kor_co_nm}.png`" class="bank-logo" alt="bank" height="60px"/>
            <v-card-title class="truncate">
              {{ product.fin_prdt_nm }}
            </v-card-title>
            <v-card-subtitle class="truncate">{{ product.kor_co_nm }}</v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useDepositStore } from "@/stores/productStores";
import { useUserStore } from "@/stores/user";
// 스토어 인스턴스 생성
const productsore = useDepositStore();
const userStore = useUserStore();

// 라우터 설정
const router = useRouter();

// 상태 관리
const isLoading = ref(true);
const selectedOption = ref(0);
const recommendedDeposits = ref([]);
const recommendedSavings = ref([]);

// 오른쪽 옵션 목록 계산
const rightOptions = computed(() => {
  const translation = userStore.choicesTranslation;

  return [
    "가장 많은 사람들이 선택한 상품",
    `${translation[userStore.UserPortFolio] || userStore.UserPortFolio.financial_goal} 목표를 위해 사람들이 선택한 상품`,
    `${translation[userStore.UserPortFolio.salary_range] || userStore.UserPortFolio.salary_range} 소득 범위의 ${translation[userStore.UserPortFolio.occupation] || userStore.UserPortFolio.occupation}들이 관심있어 하는 상품`,
    "같은 나이대의 사람들이 추천한 상품",
    ];
});

// 옵션 선택 함수
const selectOption = (index) => {
  selectedOption.value = index;
  loadRecommendations(index);
};

// 페이지 이동 함수
const navigateToPage = (url) => {
  router.push(url);
};

// 추천 데이터 로드 함수
const loadRecommendations = async (index) => {
  try {
    isLoading.value = true; // 로딩 시작
    await productsore.getRecommendations();
    const types = ["popular", "financial_goal", "occupation", "age_gender"];
    const type = types[index] || "popular";
    recommendedDeposits.value = productsore.recommenddeposits[type] || [];
    recommendedSavings.value = productsore.recommendsavings[type] || [];
  } catch (error) {
    console.error("데이터 로드 중 오류 발생:", error);
  } finally {
    isLoading.value = false; // 로딩 완료
  }
};

// 첫 번째 옵션 자동 선택 및 데이터 로드
onMounted(() => {
  selectOption(0);
});
</script>

<style scoped>
.header-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  margin-bottom: 20px;
}

.main-title {
  margin: 20px 0;
  font-weight: bold;
  font-size: 36px; /* 폰트 크기 증가 */
  text-align: center; /* 중앙 정렬 */
}

.section-title {
  margin: 30px 0 10px 0;
  font-weight: bold;
  font-size: 24px;
  text-align: left;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #666;
}

.empty-message {
  text-align: center;
  padding: 20px;
  font-size: 16px;
  color: #999;
}

.card-grid {
  margin-bottom: 20px;
}

.clickable-card {
  cursor: pointer;
}

.uniform-card {
  margin: 10px;
}

.bank-logo {
  display: block;
  margin: 0 auto 10px auto;
  max-height: 50px;
  width: 60%;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tab-selected {
  font-weight: bold;
  border-bottom: 2px solid var(--v-primary-base);
}
</style>
