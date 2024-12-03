<template>
    <div>
      <!-- 탭 내비게이션 -->
      <v-tabs v-model="tab" 
      :color="tab === 0 ? '':'primary'" 
      centered 
      :hide-slider="tab === 0">
      <v-tab @click="navigateTo('posts')" :class="{ active: tab === 1 }">작성한 글</v-tab>
      <v-tab @click="navigateTo('favorites')" :class="{ active: tab === 2 }">별무리록</v-tab>
      <v-tab @click="navigateTo('portfolio')" :class="{ active: tab === 3 }">포트폴리오</v-tab>

    </v-tabs>
  
      <!-- 탭에 따라 하위 라우트를 렌더링 -->
      <router-view />
      <div class="text-right mt-3" v-if="tab===3">
          <v-btn color="deep-purple accent-4" class="white--text" @click="goToEditPage">
            수정
          </v-btn>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import { RouterView } from 'vue-router';
  // 탭 선택 상태 관리
  const tab = ref(null);  // 여기에서 tab 변수를 제대로 정의하여 Vue가 접근할 수 있도록 합니다.
  const router = useRouter();
  const route = useRoute();
  const username = route.params.username;
  const navigateTo = (section) => {
    router.push({ name: `Profile${capitalize(section)}`, params: { username } });

  };

  const goToEditPage = () => {
    router.push({ name: "PortfolioEditView", params: { username: username } });
  };

  const capitalize = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  </script>
  
  <style scoped>
  .v-tabs {
    border-bottom: 1px solid #ccc;
  }
  
  .v-tab {
    font-weight: bold;
  }
  </style>
  