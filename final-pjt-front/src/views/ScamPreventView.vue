<!-- src/App.vue -->
<template>
    <h1 class="section-title">금융사기 안전구역</h1>
     <v-alert
          type="info"
          border="left"
          colored-border
          class="mb-4"
          v-show="!isselected"
        >
          금융사기 안전구역은 두 개의 앱으로 이루어져 있습니다! 필요한 앱을 클릭해 보세요.
        </v-alert>
    <v-app>
      <v-container class="pa-4">
        <v-row justify="center" class="mb-4">
          <v-col cols="12" sm="6" md="4">
            <v-card class="box-card" @click="moveLoan">
              <v-card-text class="box-text">대출사기 진단</v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-card class="box-card" @click="moveHouse">
              <v-card-text class="box-text">깡통전세 계산기</v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        
        <!-- 라우터 뷰 -->
        <router-view />
      </v-container>
    </v-app>
  </template>
  
  <script setup>
  import { useRouter, useRoute } from 'vue-router'
  import { computed,ref } from 'vue'
  
  const router = useRouter()
  const route = useRoute()
  
  const moveLoan = () => { 
    isselected.value=true
    router.push({ name: 'ScamLoanComponent' })
  }
  const moveHouse = () => { 
    isselected.value=true
    router.push({ name: 'HouseScamComponent' })
  }
  
  // 현재 경로가 '/'인지 확인
  const isselected = ref(false)
  </script>
  
  <style scoped>
  .box-card {
    background-color: #003366;
    color: #f5c242;
    cursor: pointer;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .box-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .box-text {
    font-size: 1.6rem;
    text-align: center;
  }
  </style>
  