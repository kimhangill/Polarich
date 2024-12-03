<template>
  <v-app>
    <v-container class="main-container" fluid>
      <v-row justify="center" align="center">
        <v-col cols="12" md="8" lg="6" class="p-0">
          <PortfolioFormComponet
            :portfolio="portfolio"
            :current-page="currentPage"
            :total-pages="totalPages"
            @submit="handleSubmit"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import PortfolioFormComponet from '@/components/PortfolioFormComponet.vue';
import { useUserStore } from '@/stores/user';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import Swal from 'sweetalert2';

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const currentPage = ref(1);
const totalPages = 3;
const portfolio = ref({
  ...userStore.userProfile.portfolio, // 작성된 포트폴리오 양식이 이미 존재하는 경우 사용
  username: userStore.userProfile.username,
  token: userStore.token,
});

const handleSubmit = async (portfolioData) => {
  console.log('요청 받았어요.');
  
  try {
    const url = `http://127.0.0.1:8000/api/v1/accounts/portfolio/${userStore.userProfile.username}/`;
    const method = 'post';
    const response = await axios({
      method,
      url,
      data: portfolioData,
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    }).then((res)=>console.log(res.data)
    );

    Swal.fire({
      icon: 'success',
      title: '성공',
      text: '포트폴리오가 성공적으로 제출되었습니다!',
      confirmButtonText: '확인',
    });
      router.push({ name: 'MainView' });
  } catch (error) {
    console.error('포트폴리오 제출 중 오류 발생:', error);
    Swal.fire({
      icon: 'error',
      title: '제출 실패',
      text: '포트폴리오 제출에 실패하였습니다. 다시 시도해주세요.',
      confirmButtonText: '확인',
    });
  }
};
</script>