<template>
  <div>
    <div class="portfolio-section">
      <h3 class="section-title mt-3">{{ userStore.userNickname }}님의 재무 포트폴리오</h3>
      <v-row v-if="portfolioDetails?.length">
        <v-col
          v-for="(detail, index) in portfolioDetails"
          :key="index"
          cols="12"
          md="6"
          lg="4"
          class="mb-4"
        >
          <div class="portfolio-item">
            <h4 class="portfolio-item-title">{{ detail.title }}</h4>
            <p class="portfolio-item-subtitle">{{ detail.subtitle }}</p>
          </div>
        </v-col>
      </v-row>
      <div v-else>
        <v-alert type="info" dismissible>
          포트폴리오 정보가 없습니다.
        </v-alert>
      </div>

      <!-- 수정 버튼 추가 -->
      <div class="text-right mt-3">
        <v-btn color="deep-purple accent-4" class="white--text" @click="goToEditPage">
          수정
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { RouterView, useRouter } from "vue-router";
import axios from "axios";
import Swal from "sweetalert2";

const userStore = useUserStore();
const router = useRouter();
const portfolio = ref({}); // 포트폴리오 정보를 저장할 객체

// 포트폴리오 세부 항목 정의
const portfolioDetails = ref([
  { title: "연봉 범위", subtitle: "salary_range" },
  { title: "직업", subtitle: "occupation" },
  { title: "투자 성향", subtitle: "investment_risk_profile" },
  { title: "재무 목표", subtitle: "financial_goal" },
  { title: "투자 경험", subtitle: "experience_years" },
  { title: "선호하는 투자 기간", subtitle: "preferred_investment_period" },
  { title: "유동성 선호 여부", subtitle: "liquidity_preference" },
  { title: "위험 수용도", subtitle: "risk_tolerance" },
  { title: "월 저축액", subtitle: "monthly_savings" },
  { title: "부채 비율", subtitle: "debt_ratio" },
  { title: "선호하는 투자 유형", subtitle: "preferred_investment_type" },
]);

// 포트폴리오 데이터를 가져온 후 업데이트


// 페이지가 로드될 때 포트폴리오 정보를 가져오는 함수
const fetchPortfolio = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/accounts/profiles/${userStore.userProfile.username}/portfolio/`,
      {
        headers: {
          Authorization: `Token ${userStore.token}`, // 토큰 인증 방식
        },
      }
    );

    portfolio.value = response.data;
    portfolioDetails.value.forEach((item) => {
      
      item.subtitle = userStore.choicesTranslation[portfolio.value[item.subtitle]] || null
});

  } catch (error) {
    console.error("포트폴리오 정보 가져오기 중 오류 발생:", error);
    Swal.fire({
      icon: "error",
      title: "불러오기 실패",
      text: "포트폴리오 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.",
      confirmButtonText: "확인",
    });
  }
};

// 수정 페이지로 이동하는 함수
const goToEditPage = () => {
  router.push({ name: "PortfolioEditView", params: { username: userStore.userProfile.username } });
};

// 컴포넌트가 마운트될 때 포트폴리오 정보 가져오기
onMounted(fetchPortfolio);
</script>

<style scoped>
.portfolio-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #003366; /* 어두운 블루 색상 */
  border-bottom: 2px solid #f5c242; /* 골드 색상으로 하단 테두리 추가 */
  padding-bottom: 0.5rem;
}

.portfolio-item {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: transform 0.3s, box-shadow 0.3s;
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
}

.portfolio-item-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #001f3f;
}

.portfolio-item-subtitle {
  font-size: 1rem;
  color: #555;
}

.v-btn {
  min-width: 100px;
  background-color: #001f3f; /* 어두운 파랑 배경 */
  &:hover {
    background-color: #003366; /* 호버 시 조금 더 밝은 색상 */
  }
}
</style>
