<template>
  <div>
    <div class="favorites-section">
      <h3 class="section-title mt-3">{{nickname}}님과 폴라리치 유저와의 상품금리 비교</h3>
      <div>
      <canvas ref="rateBarChart"></canvas>
      </div>
      <h3 class="section-title mt-3">{{nickname}}님이 담은 금융 길잡이별</h3>
      <v-row v-if="userSavings?.length || userDeposits?.length">
        <v-col
          v-for="saving in userSavings"
          :key="saving.id"
          cols="12"
          md="6"
          lg="4"
          class="mb-4"
        >
          <v-card>
            <v-card-title>{{ saving.kor_co_nm }}</v-card-title>
            <v-card-subtitle>{{ saving.fin_prdt_nm }}</v-card-subtitle>
            <v-card-text>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                text
                @click="gotoProductDetail(saving.id, 'saving')"
              >
                자세히 보기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col
          v-for="deposit in userDeposits"
          :key="deposit.id"
          cols="12"
          md="6"
          lg="4"
          class="mb-4"
        >
          <v-card>
              <v-card-title>{{ deposit.kor_co_nm }}</v-card-title>
            <v-card-subtitle>{{ deposit.fin_prdt_nm }}</v-card-subtitle>
            <v-card-text>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                text
                @click="gotoProductDetail(deposit.id, 'deposit')"
              >
                자세히 보기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <div v-else>
        <v-alert type="info" dismissible>
          별무리가 텅 비어 있어요.
        </v-alert>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted,ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useDepositStore } from '@/stores/productStores';
import axios from 'axios';
import { Chart } from 'chart.js/auto';

const router = useRouter();
const userStore = useUserStore();
const depositstore = useDepositStore();
const nickname = userStore.userNickname
const userSavings = computed(() => depositstore.userSavings);
const userDeposits = computed(() => depositstore.userDeposits);
const my_deposit = ref(0);
const my_saving = ref(0);
const avg_deposit = ref(0);
const avg_saving = ref(0);
const rateBarChart = ref(null)

const gotoProductDetail = (id, type) => {
  router.push({ name: 'ProductDetailView', params: { id, type } });
};






onMounted(async () => {
  await depositstore.getFavorites();
  if (!userStore.userProfile.username) {
    userStore.getProfile();
  }
  await axios({
      method:'get',
      url:'http://127.0.0.1:8000/api/v1/accounts/avg/',
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    }).then((res)=>{
      console.log(res.data);
      my_deposit.value=res.data.my_avg_deposit
      my_saving.value=res.data.my_avg_saving
      avg_deposit.value=res.data.avg_deposit
      avg_saving.value=res.data.avg_saving
      new Chart(rateBarChart.value,{
        type: "bar",
        data: {
          labels: ["예금", "적금"],
          datasets: [                  {
                  label: "내가 담은 상품",
                  data: [my_deposit.value, my_saving.value],
                  backgroundColor: "#4caf50",
                  borderWidth: 1,
                },
                {
                  label: "전체 평균",
                  data: [avg_deposit.value, avg_saving.value],
                  backgroundColor: "#ff9800",
                  borderWidth: 1,
                }]
        },
        options: {
        indexAxis: "y", // 가로 막대그래프
        scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: "금리 (%)",
         },
       },
        y: {
          title: {
           display: true,

         },
       },
      },
      plugins: {
        legend: {
          display: true,
        },
     },
    }
  })
    }).catch((err)=>console.log(err))
});
</script>

<style scoped>
.favorites-section {
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
</style>
