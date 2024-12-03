<template>
  <v-app>
    <!-- 상단 바 -->
    <v-app-bar flat color="#003366">
    <v-container>
      <v-row align="center" justify="space-between" class="gap-md-4" style="padding: 0 24px;">
        <!-- 햄버거 메뉴 버튼 -->
        <v-btn icon @click="drawer = !drawer" color="#f5c242">
          <v-icon>mdi-menu</v-icon>
        </v-btn>

        <!-- 로고 -->
        <v-tab @click="moveMain" class="d-flex align-center">
          <span style="color: #f5c242; font-weight: bold; font-size: 2rem;">Polarich</span>
        </v-tab>

        <!-- 검색 -->
        <v-col cols="auto" class="d-flex align-center" style="flex-grow: 1; position: relative;">
            <v-text-field
              v-model="search"
              placeholder="통합 검색"
              solo-inverted
              hide-details
              flat
              full-width
              color="#f5c242"
              class="elevation-2 text-white"
              dense
              prepend-inner-icon="mdi-magnify"
              style="--v-placeholder-opacity: 1; color: white;"
              @keyup.enter="moveSearch"
            ></v-text-field>

            <!-- 최근 검색어 리스트 -->
            <!-- <v-card v-show="isSearchMenuOpen" class="search-menu-card">
              <v-card-title>최근 검색어</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item v-for="(item, index) in userStore.recentsearch" :key="index">
                    <v-list-item-content>{{ item }}</v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card> -->
          </v-col>



        <!-- 프로필 영역 -->
        <v-menu offset-y>
          <template v-slot:activator="{ props }">
            <div class="d-flex align-center" v-bind="props" style="cursor: pointer;">
              <h3 class="mx-3">{{ user.nickname }}</h3>
              <v-avatar size="36" class="me-2 elevation-3" style="border: 2px solid #f5c242">
                <img v-if="isLogIn" :src="'http://127.0.0.1:8000' + user.profileImage" width="100%" height="100%" alt="프로필 이미지" />
                <img v-else="isLogIn" src="./assets/profile.png" width="100%" height="100%" alt="프로필 이미지" />
              </v-avatar>
              <v-icon class="arrow-icon ms-1" icon="mdi-menu-down" size="24"></v-icon>
            </div>
          </template>
          <!-- 메뉴 리스트 -->
          <v-list>
            <v-list-item @click="moveProfile">회원정보</v-list-item>
            <v-list-item @click="handleSignup">회원가입</v-list-item>
            <v-list-item @click="!isLogIn ? Login() : Logout()">
              {{ !isLogIn ? "로그인" : "로그아웃" }}
            </v-list-item>
          </v-list>
        </v-menu>
      </v-row>
    </v-container>
  </v-app-bar>

  <!-- 사이드바 -->
  <v-navigation-drawer v-model="drawer" app temporary overlay color="#ffffff">
    <v-list>
      <!-- 로고 및 사이드바 헤더 -->
      <v-list-item class="d-flex align-center">
        <v-tab @click="moveMain" class="logo" style="color: #f5c242; font-weight: bold; font-size: 2rem;">
          Polarich
        </v-tab>
      </v-list-item>
    </v-list>
    <v-list>
      <v-list-item-group>
        <!-- 대분류 제목 -->
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="section-title">금융 상품</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- 금융상품 메뉴 -->
        <v-list-item @click="moveDeposits">
          <v-list-item-title>예금</v-list-item-title>
        </v-list-item>
        <v-list-item @click="moveSavings">
          <v-list-item-title>적금</v-list-item-title>
        </v-list-item>
        <v-list-item @click="moveLoan">
          <v-list-item-title>대출</v-list-item-title>
        </v-list-item>

      </v-list-item-group>
      <v-list-item-group>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="section-title" >은행 찾기</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- 은행 찾기 메뉴 -->
        <v-list-item  @click="moveMap">
          <v-list-item-title>내 주변 은행</v-list-item-title>
        </v-list-item>

      </v-list-item-group>

      <v-list-item-group>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="section-title">환율</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- 환율 메뉴 -->
        <v-list-item @click="moveExchange">
          <v-list-item-title>환율</v-list-item-title>
        </v-list-item>

      </v-list-item-group>

      <v-list-item-group>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="section-title">추천 페이지</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- 추천 페이지 메뉴 -->
        <v-list-item @click="moveRecommendPage">
          <v-list-item-title>추천 페이지</v-list-item-title>
        </v-list-item>
        <v-list-item @click="moveScamPrevent">
          <v-list-item-title>금융사기 안전구역</v-list-item-title>
        </v-list-item>

      </v-list-item-group>

      <v-list-item-group>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="section-title">커뮤니티</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- 커뮤니티 메뉴 -->
        <v-list-item @click="moveCommunity('general')">
          <v-list-item-title>자유게시판</v-list-item-title>
        </v-list-item>
        <v-list-item @click="moveCommunity('qna')">
          <v-list-item-title>Q&A 게시판</v-list-item-title>
        </v-list-item>
        <v-list-item @click="moveCommunity('column')">
          <v-list-item-title>칼럼 게시판</v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>

    <!-- 페이지 콘텐츠 -->
    <v-main>
      <v-container class="main-container" 
      :class="{'background-image': isBackgroundView}">
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>


<script setup>
import { computed,ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
import swal from "sweetalert";
import bgImage from "@/assets/bgbg.jpg"
const userStore = useUserStore();
const search = ref('')
const isSearchMenuOpen = ref(false);
const router = useRouter();
const drawer = ref(false)
const isLogIn = computed(() => userStore.isLogin);
const user = computed(() => userStore.userProfile || "로그인");
const moveMain = () => router.push({ name: "MainView" });
const moveCommunity = (type) => {
  router.push({
    name: "CommunityTypeView", // 공통 컴포넌트로 이동
    params: { type }, // type 파라미터 전달
  });
};
const moveSearch = () => {
  if (search.value.trim() !== '') {
    router.push({ name: "SearchView", query: { q: search.value.trim() } });
  }
};
const moveLoan = () => router.replace({name:'LoanList'})
const moveProfile = () => router.push({ name: "ProfilePage",params:{username:userStore.userProfile.username} });
const handleSignup = () => router.push({ name: "SignupView" });
const Login = () => router.push({ name: "LoginView" });
const moveDeposits = function () {router.replace({ name: "DepositProductsView" });};
const moveSavings = function () {router.replace({ name: "SavingProductsView" });};
const moveMap = function () {router.replace({ name: "MapView" });}
const moveExchange = () => router.push({ name: "ExchangeView" });
const moveRecommendPage = () => router.push({ name: "RecommendPageView" });
const moveScamPrevent = function () {router.push({ name: "ScamPreventView" });};
const openSearchMenu = () => {
  isSearchMenuOpen.value = true;
  document.body.classList.add('blur-background');
};

const closeSearchMenu = () => {
  isSearchMenuOpen.value = false;
  document.body.classList.remove('blur-background');
};
const Logout = () => {
  swal({
    title: "로그아웃 하시겠습니까?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      swal("로그아웃되었습니다.", { icon: "success" });
      userStore.logout();
    }
  });
};

const route = useRoute()

const isBackgroundView = computed(() =>
  ['LoginView', 'SignupView'].includes(route.name)
);

</script>

<style>


.logo {
  width: 100%;
  font-size: 1.5rem;
  color: hsl(51, 60%, 38%);

  cursor: pointer;
}
.user-name {
  font-weight: bold;
}
.navigation-tabs {
  flex-grow: 1;
}
.search-tab {
  margin-right: 20px;
}



.main-container {
  max-width: 60%;
  margin: 0 auto;
  padding: 10px;
  box-sizing: border-box;
}
.main-container.background-image {
  max-width: 100%;
}
.background-image {
  max-width: 100%;
  background-image: url('../src/assets/bgbg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
}
.extend {
  color: #003366;
  font-weight: bold;
}
.search-menu-card {
  position: absolute;
  top: calc(100% + 8px); /* 검색창 바로 밑에 여백 추가 */
  left: 0;
  width: 10px;
  z-index: 9999; /* 높은 z-index 설정 */
  transform: translateY(4px);
  box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.2); /* 약간의 그림자 추가 */
}

.v-col {
  position: relative;
  z-index: 20; /* 검색창과 관련된 요소가 위로 보이도록 설정 */
}



</style>

