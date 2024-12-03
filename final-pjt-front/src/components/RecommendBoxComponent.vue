<template>
    <v-container>
      <!-- 데이터 로딩 상태 -->
      <div v-if="isLoading" class="loading">
        데이터를 불러오는 중입니다...
      </div>
  
      <!-- 데이터 로드 후 렌더링 -->
      <template v-else>
        <!-- 예금 섹션 -->
        <h2 v-if="recommendedDeposits.length" class="section-title">
          추천 예금 상품
        </h2>
        <div v-else class="empty-message">
          아직 길잡이별이 충분히 빛나지 않았어요
        </div>
  
        <!-- 예금 섹션 슬라이드 -->
        <v-slide-group
          v-if="recommendedDeposits.length"
          show-arrows
          class="my-carousel"
        >
          <v-slide-group-item
            v-for="product in recommendedDeposits"
            :key="'deposit-product-' + product.id"
          >
            <v-card
              class="clickable-card uniform-card"
              @click="navigateToPage(`/deposit/${product.id}`)"
            >
              <img :src="`../src/assets/bank/${product.kor_co_nm}.png`" class="mx-auto" alt="bank" height="120" width="60%" />
              <v-card-title class="truncate">
                {{ product.fin_prdt_nm }}
              </v-card-title>
              <v-card-subtitle class="truncate">{{ product.kor_co_nm }}</v-card-subtitle>
            </v-card>
          </v-slide-group-item>
        </v-slide-group>
  
        <!-- 적금 섹션 -->
        <h2 v-if="recommendedSavings.length" class="section-title">
          추천 적금 상품
        </h2>
  
        <!-- 적금 섹션 슬라이드 -->
        <v-slide-group
          v-if="recommendedSavings.length"
          show-arrows
          class="my-carousel"
        >
          <v-slide-group-item
            v-for="product in recommendedSavings"
            :key="'saving-product-' + product.id"
          >
            <v-card
              class="clickable-card uniform-card"
              @click="navigateToPage(`/saving/${product.id}`)"
            >
              <img :src="`../src/assets/bank/${product.kor_co_nm}.png`" class="mx-auto" alt="bank" height="120" width="60%" />
              <v-card-title class="truncate">
                {{ product.fin_prdt_nm }}
              </v-card-title>
              <v-card-subtitle class="truncate">{{ product.kor_co_nm }}</v-card-subtitle>
              <v-card-text class="truncate">{{ product.etc_note }}</v-card-text>
            </v-card>
          </v-slide-group-item>
        </v-slide-group>
      </template>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from "vue";
  import { useRouter } from "vue-router";
  import { useDepositStore } from "@/stores/productStores";
  
  // Props로 추천 타입 받기
  const props = defineProps({ type: String });
  
  // 라우터 설정
  const router = useRouter();
  
  // 로딩 상태
  const isLoading = ref(true);
  const recommendedDeposits = ref([]);
  const recommendedSavings = ref([]);
  const depositStore = useDepositStore();
  
  // 페이지 이동 함수
  const navigateToPage = (url) => {
    router.push(url);
  };
  
  // 데이터 로드 함수
  const loadRecommendations = async () => {
    try {
      isLoading.value = true; // 로딩 시작
      const type = props.type || "popular";
      await depositStore.getRecommends(type);
      recommendedDeposits.value = depositStore.recommenddeposits;
      recommendedSavings.value = depositStore.recommendsavings;
    } catch (error) {
      console.error("데이터 로드 중 오류 발생:", error);
    } finally {
      isLoading.value = false; // 로딩 완료
    }
  };
  
  // 타입이 변경될 때마다 데이터 로드
  watch(() => props.type, () => {
    loadRecommendations();
  });
  
  // 컴포넌트 마운트 시 데이터 로드
  onMounted(() => {
    loadRecommendations();
  });
  </script>
  
  <style scoped>
  .loading {
    text-align: center;
    padding: 20px;
    font-size: 18px;
    color: #666;
  }
  .section-title {
    margin: 20px 0;
    font-weight: bold;
  }
  .empty-message {
    text-align: center;
    padding: 20px;
    font-size: 16px;
    color: #999;
  }
  .my-carousel {
    margin-bottom: 20px;
  }
  .clickable-card {
    cursor: pointer;
  }
  .uniform-card {
    max-width: 300px;
    margin: 10px;
  }
  .truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  </style>
  