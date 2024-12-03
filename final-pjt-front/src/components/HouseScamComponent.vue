<template>
  <v-container>
    <h3 class="display-1 text-center mb-4 section-title">깡통전세 계산기</h3>

    <!-- Step 1: 주소 입력 -->
    <v-card elevation="3" class="pa-6 mt-4">
      <v-row>
        <v-col cols="12">
          <p>Step 1. 관심이 있는 주택의 주소 정보를 입력해주세요.</p>
          <v-alert type="info" border="left" colored-border>
            <h3>주소 정보:</h3>
            <p>주택명: <strong>{{ buildingName }}</strong></p>
            <p>우편번호: <strong>{{ bcode }}</strong></p>
            <p>기본주소: <strong>{{ address01 }}</strong></p>
          </v-alert>
          <div ref="embed"></div>
          <v-btn @click="showApi" color="primary" class="mt-4">주소 찾기</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- Step 2: 주택 정보 입력 -->
    <v-card elevation="3" class="pa-6 mt-4">
      <v-row>
        <v-col cols="12">
          <p>Step 2. 관심이 있는 주택의 거주유형, 전세가, 선순위 근저당을 입력해주세요</p>
          <v-row>
            <v-col cols="12">
              <v-label>주택 유형</v-label>
              <v-radio-group v-model="type" class="mt-2">
                <v-radio label="아파트" value="아파트"></v-radio>
                <v-radio label="연립다세대주택(빌라)" value="연립다세대주택"></v-radio>
              </v-radio-group>
            </v-col>
            <v-col cols="12" class="mt-3">
              <v-label for="price">주택 전세가(만원)</v-label>
              <v-text-field v-model="price" placeholder="전세가를 입력해주세요" outlined></v-text-field>
            </v-col>
            <v-col cols="12" class="mt-3">
              <v-label for="debt">선순위 근저당 (선택)</v-label>
              <v-text-field v-model="debt" placeholder="선순위 근저당 금액을 입력해주세요" outlined></v-text-field>
              <p class="text-blue small text-muted">선순위 근저당이 없을 경우, 공란으로 두세요. 주택에 대한 선순위근저당은 가까운 관공서 혹은 정부24를 통한 등기부등본 발급으로 확인하실 수 있습니다.</p>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row class="mt-4">
        <v-col cols="12" class="text-right">
          <v-btn @click="calculate" :loading="isLoading" color="warning" large>계산하기</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- 로딩 스피너 -->
    <v-dialog v-model="isLoading" hide-overlay persistent width="300">
      <v-card color="primary" dark>
        <v-card-text class="text-center">
          <v-progress-circular indeterminate color="white"></v-progress-circular>
          <p>계산 중입니다. 잠시만 기다려주세요...</p>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Step 3: 실거래가 입력 (데이터 없을 경우) -->
    <v-card v-if="isStepThree" elevation="3" class="pa-6 mt-4">
      <v-row>
        <v-col cols="12">
          <v-alert type="warning" border="left" colored-border>
            <p>최근 3년간 국토교통부 매매기록에 해당 매물을 찾지 못하였습니다.</p>
          </v-alert>
          <p>실거래가를 직접 입력해주세요.</p>
          <v-text-field v-model="origin_price" placeholder="실거래가를 입력해주세요" outlined></v-text-field>
          <v-btn @click="confirmResult" color="warning" class="mt-4">결과 확인</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- 결과 표시 -->
    <v-card v-if="isResultVisible" elevation="3" class="pa-6 mt-4">
      <v-row>
        <v-col cols="12">
          <v-alert :type="resultAlertType" border="left" colored-border>
            <h3 class="section-title">{{ buildingName }}의 최근 3년 평균 실거래가: {{ origin_price }}만원</h3>
            <p>{{ resultMessage }}</p>
            <v-btn @click="goToLink" color="primary" class="mt-2 mx-auto">관련 게시물 읽어보기</v-btn>
          </v-alert>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';

const type = ref('');
const price = ref(0);
const debt = ref(0);
const buildingName= ref('')
const bcode = ref('');
const address01 = ref('');
const dong = ref('');
const jibun = ref('');
const showApi = () => {
  new window.daum.Postcode({
    oncomplete: (data) => {
      bcode.value = data.bcode.slice(0,5);
      address01.value = data.address;
      jibun.value  = data.jibunAddressEnglish;
      dong.value = data.bname;
      buildingName.value = data.buildingName
    },
  }).open();
};

const userstore = useUserStore();

const origin_price = ref('');
const isStepThree = ref(false);
const isResultVisible = ref(false);
const resultMessage = ref('');
const resultAlertType = ref('');
const isLoading = ref(false);

const calculate = function () {
  isLoading.value = true; // 로딩 시작
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/products/checkhouse',
    params: {
      type: type.value,
      address: bcode.value,
      jibun: jibun.value.split(' ')[0],
      dong: dong.value,
    },
    headers: {
      Authorization: `Token ${userstore.token}`
    }
  })
    .then((res) => {
      if (res.data.length > 0) {
        // price 값의 평균 계산
        let totalPrice = 0;
        res.data.forEach((item) => {
          let priceNum = Number(item.price.replace(/,/g, ''));
          totalPrice += priceNum;
        });
        origin_price.value = (totalPrice / res.data.length).toFixed(0);
        // 결과 확인
        checkPrice();
      } else {
        isStepThree.value = true;
      }
      isLoading.value = false; // 로딩 종료
    })
    .catch((err) => {
      console.log(err);
      isStepThree.value = true;
      isLoading.value = false; // 로딩 종료
    });
};

const checkPrice = () => {

  const totalPrice = Number(price.value) + Number(debt.value || 0);
  const originPrice70 = Number(origin_price.value) * 0.7;

  if (totalPrice > originPrice70) {
    // 70%를 넘을 때
    resultMessage.value = '해당 매물은 깡통전세 위험군에 해당하는 가격을 형성하고 있습니다!\n해당 매물에 대한 문제가 발생할 경우, 전세금 반환 보증에 문제가 생길 수 있습니다.';
    resultAlertType.value = 'orange';
  } else {
    // 70%를 넘지 않을 때
    resultMessage.value = '해당 매물은 깡통전세 위험군에 해당하지 않는 가격을 형성하고 있습니다!\n그러나, 전세사기의 경우 가격 확인 외 다양한 요소가 문제될 수 있으므로, 자세한 사항은 아래 칼럼을 확인하세요!';
    resultAlertType.value = 'success';
  }
  isResultVisible.value = true;
};

const confirmResult = () => {
  // 사용자가 입력한 origin_price로 결과 확인
  checkPrice();
};

const goToLink = () => {
  // 바로가기 클릭 시 실행될 함수 (현재는 console.log)
  console.log('바로가기 클릭됨');
};
</script>

<style scoped>
.v-alert {
  padding: 20px;
  margin-bottom: 15px;
}
button {
  margin-top: 20px;
}
.v-label {
  font-weight: 500;
  color: #333;
}
.text-muted {
  font-size: 0.85rem;
  color: #666;
}

.section-title {
  /* font-size: 1.8rem; */
  font-weight: bold;
  color: white; /* 어두운 블루 색상 */
  border-bottom: 2.5px solid #f5c242; /* 골드 색상으로 하단 테두리 추가 */
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
