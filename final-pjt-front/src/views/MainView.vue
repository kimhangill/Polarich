<template>
  <v-app>
    <v-main>
      <div class="background-image-container">
        <!-- Your website content goes here -->
        <v-container>
          <v-row>
            <v-col>
              <h1 class="text-white header-large"><span style="color: #f5c242;">POLARICH</span> <br> Your Financial<br> Guiding Star</h1>
              <p class="text-white" style="font-size: 2rem; font-weight: bold;">차가운 금융의 세계, 당신의 하나뿐인 길잡이별</p>
            </v-col>
          </v-row>
        </v-container>
      </div>
      <!-- Highlight section between image and cards -->
      <v-container class="highlight-message">
        <v-row>
          <v-col>
            <h2 class="section-title highlight-text">별빛 아래, 당신의 금융 여정을 빛내드립니다</h2>
          </v-col>
        </v-row>
      </v-container>
      <!-- Scrollable content section -->
      <v-container class="scrollable-content">
        <v-row>
          <v-col cols="12">
            <div class="feature-section" style="background-color: #b0c4de; height: 40vh; position: relative;">
              <div class="feature-text">
                <h1>환율 실시간 계산기</h1>
                <p>최적의 환전 시점을 실시간으로 찾아보세요.</p>
              </div>
              <div class="feature-icon-large-right">
                <v-icon size="256" color="#003366">mdi-currency-usd</v-icon>
              </div>
              <v-btn color="primary" class="feature-btn fixed-bottom-right" @click="moveExchange">바로가기</v-btn>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="feature-section" style="background-color: #ffcccb; height: 40vh; position: relative;">
              <div class="feature-text">
                <h1>내 주변 은행 찾기</h1>
                <p>가장 가까운 은행을 위치 기반으로 쉽게 찾을 수 있습니다.</p>
              </div>
              <div class="feature-icon-large-right">
                <v-icon size="256" color="#003366">mdi-bank</v-icon>
              </div>
              <v-btn color="primary" class="feature-btn fixed-bottom-right" @click="moveMap">바로가기</v-btn>
            </div>
          </v-col>
          <v-container class="highlight-message">
        <v-row>
          <v-col>
            <h2 class="section-title highlight-text">당신이 원하는 금융 정보를, 가장 빠르게 찾아보세요.</h2>
          </v-col>
        </v-row>
      </v-container>
          <v-col cols="12">
            <div class="feature-section" style="background-color: #e6e6fa; height: 40vh; position: relative;">
              <v-row>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-bank</v-icon>
                    <v-card-title class="submenu-title">예금</v-card-title>
                    <v-card-text>다양한 예금 상품을 제공합니다.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn" @click="moveDeposits">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-cash-multiple</v-icon>
                    <v-card-title class="submenu-title">적금</v-card-title>
                    <v-card-text>적금을 쌓아 미래를 준비하세요.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn" @click="moveSavings">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-handshake</v-icon>
                    <v-card-title class="submenu-title">대출</v-card-title>
                    <v-card-text>현명한 대출으로 필요를 충족하세요.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn" @click="moveLoans">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-col>
          <v-container class="highlight-message">
        <v-row>
          <v-col>
            <h2 class="section-title highlight-text">폴라리치의 별빛 아래서, 여정을 함께하는 사람들을 만날 수 있어요.</h2>
          </v-col>
        </v-row>
      </v-container>
          <v-col cols="12">
            <div class="feature-section" style="background-color: #add8e6; height: 40vh; position: relative;">
              <v-row>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-forum</v-icon>
                    <v-card-title class="submenu-title">자유게시판</v-card-title>
                    <v-card-text>다양한 주제에 대해 자유롭게 소통하세요.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn"  @click="moveCommunity('general')">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-book-open-variant</v-icon>
                    <v-card-title class="submenu-title">칼럼게시판</v-card-title>
                    <v-card-text>전문가들의 칼럼 게시판.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn"  @click="moveCommunity('column')">바로가기</v-btn>
                    </v-card-actions>
                    </v-card>
                </v-col>
                <v-col cols="4">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-comment-question-outline</v-icon>
                    <v-card-title class="submenu-title">QnA 게시판</v-card-title>
                    <v-card-text>궁금한 점을 질문하고 답변을 받아보세요.</v-card-text>
                    <v-card-actions>
                      <v-btn color="light" class="submenu-btn redesigned-btn" @click="moveCommunity('qna')">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-col>
          <v-container class="highlight-message">
        <v-row>
          <v-col>
            <h2 class="section-title highlight-text">가장 안전하고 확실한 길로 이끄는 금융 길잡이별이 될게요.</h2>
          </v-col>
        </v-row>
      </v-container>
          <v-col cols="12">
            <div class="feature-section" style="background-color: #ffe4b5; height: 40vh; position: relative;">
              <v-row>
                <v-col cols="6">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-thumb-up-outline</v-icon>
                    <v-card-title class="submenu-title">금융상품 추천</v-card-title>
                    <v-card-text>개인 맞춤형 금융상품을 추천받으세요.</v-card-text>
                    <v-card-actions>
                      <v-btn @click="moveRecommendPage" color="light" class="submenu-btn redesigned-btn">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="6">
                  <v-card class="submenu-card redesigned-card">
                    <v-icon size="150" color="#003366">mdi-shield-check</v-icon>
                    <v-card-title class="submenu-title">금융사기 안전구역</v-card-title>
                    <v-card-text>금융사기 위험으로부터 자신을 보호하세요.</v-card-text>
                    <v-card-actions>
                      <v-btn @click="moveScamPrevent" color="light" class="submenu-btn redesigned-btn">바로가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import swal from "sweetalert";
const userStore = useUserStore();
const router = useRouter();
const moveMap = () => {
  router.push({ name: "MapView" });
};
const moveExchange = () => {
  router.push({ name: "ExchangeView" });
};
const moveRecommendPage = () => {router.push({ name: "RecommendPageView" });};
const moveDeposits = function () {router.push({ name: "DepositProductsView" });};
const moveSavings = function () {router.push({ name: "SavingProductsView" });};
const moveLoans = function () {router.push({ name: "LoanProductView" });};
const moveScamPrevent = function () {router.push({ name: "ScamPreventView" });};

const moveCommunity = (type) => {
  router.push({
    name: "CommunityTypeView", // 공통 컴포넌트로 이동
    params: { type }, // type 파라미터 전달
  });
};

</script>
<style scoped>
.background-image-container {
  background-image: url('@/assets/bgbg.jpg');
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 55vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.header-large {
  font-size: 7rem;
  font-weight: bold;
}

.highlight-message {
  margin: 30px 0;
  text-align: center;
}

.highlight-text {
  color: #003366;
  font-size: 2.5rem;
  font-weight: bold;
}

.scrollable-content {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.feature-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.3s ease;
  position: relative;
}

.feature-text {
  position: absolute;
  top: 20px;
  left: 20px;
  color: #003366;
}

.feature-icon-large-right {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
}

.feature-btn {
  position: absolute;
  bottom: 20px;
  right: 20px;
  color: #ffffff;
}

.fixed-bottom-right {
  position: absolute;
  bottom: 20px;
  right: 20px;
}

.submenu-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.3s ease;
  position: relative;
}

.submenu-text {
  color: #003366;
  font-weight: bold;
}

.redesigned-card {
  background-color: #f9f9fb;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: auto;
}

.redesigned-btn {
  background-color: #007bff;
  color: #ffffff;
  padding: 10px 15px;
  border-radius: 5px;
}

.submenu-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 15px;
}
</style>



