<template>
  <v-container>
    <!-- 헤더 영역 -->
      <v-spacer></v-spacer>
    <!-- 주요 환율 표시 -->
    <h1 class="section-title text-center">오늘의 주요국 환율</h1>
    <v-row class="mt-5" justify="center" style="gap: 16px;">
      <v-card v-for="currency in popularCurrencies" :key="currency.code" outlined>
        <v-card-text class="text-center">
          <!-- 나라 이미지 -->
          <div style="margin-bottom: 10px;">
            <span style="font-size: 50px;">
    {{ currency.country === 'usa' ? '🇺🇸' : (currency.country === 'cn' ? '🇨🇳' : (currency.country === 'jp' ? '🇯🇵' : '🌍')) }}
  </span>
          </div>
          <h3>{{ currency.name }}</h3>
          <p>1 {{ currency.code }} = {{ currency.rate }} 원</p>
        </v-card-text>
      </v-card>
    </v-row>

    <!-- 환율 계산기 섹션 -->
    <div class="d-flex flex-column mt-5" style="gap: 16px; max-width: 50%; margin: auto;">
      <!-- 기준 통화 -->
      <v-col cols="12">
        <v-select
          v-model="baseCurrency"
          :items="currencyOptions"
          label="1. 기준 통화"
          dense
        ></v-select>
      </v-col>
      <!-- 변환 통화 -->
      <v-col cols="12">
        <v-select
          v-model="targetCurrency"
          :items="currencyOptions"
          label="2. 변환 통화"
          dense
        ></v-select>
      </v-col>
      <!-- 변환할 금액 -->
      <v-col cols="12">
        <v-text-field
          v-model="amount"
          :placeholder="'금액 입력'"
          label="3. 변환할 금액"
          type="number"
          dense
        ></v-text-field>
      </v-col>
      <!-- 결과 -->
      <v-col cols="12">
        <h3>결과</h3>
        <p v-if="conversionResult" class="result-text">
          {{ conversionResult }} 
          <v-divider></v-divider>
          {{ targetCurrency }}
        </p>
        <p v-else>결과가 여기에 표시됩니다.</p>
      </v-col>
    </div>

    <!-- 실시간 환율 목록 -->
    <v-row justify="center" class="mt-5">
      <v-btn color="primary" @click="toggleExchangeList" class="mb-5">
        {{ showExchangeList ? "실시간 환율 목록 보기" : "실시간 환율 목록 숨기기" }}
      </v-btn>
    </v-row>

    <v-slide-y-transition>
      <v-data-table
        v-if="!showExchangeList"
        :items="filteredExchangeRates"
        :headers="headers"
        class="elevation-1"
        dense
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-text-field
              v-model="searchQuery"
              label="통화명 검색"
              prepend-inner-icon="mdi-magnify"
              outlined
              dense
            ></v-text-field>
          </v-toolbar>
        </template>
      </v-data-table>
    </v-slide-y-transition>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";

// 환율 데이터를 저장할 변수
const exchangeRates = ref([]);
const searchQuery = ref("");
const showExchangeList = ref(true); // 목록 표시 여부, 기본적으로 표시

// 계산 관련 변수
const baseCurrency = ref("");
const targetCurrency = ref("");
const amount = ref(null); // 초기 값을 null로 설정
const conversionResult = ref(null);

// 주요 환율 표시할 국가 리스트
const popularCurrencies = ref([
  { name: "미국 달러 (USD)", code: "USD", rate: null, image: "src/assets/usa.png", country:'usa' },
  { name: "중국 위안 (CNY)", code: "CNH", rate: null, image: "src/assets/china.png",country:'cn' },
  { name: "일본 엔 (JPY)", code: "JPY(100)", rate: null, image: "src/assets/japan.png",country:'jp' },
]);

// 테이블 헤더 정의
const headers = [
  { title: "ID", value: "id" },
  { title: "통화명 (통화 코드)", value: "cur_nm_with_code" },
  { title: "매매", value: "tts" },
  { title: "매수", value: "ttb" },
  { title: "날짜", value: "date" },
];

// 검색 필터링된 데이터
const filteredExchangeRates = computed(() =>
  exchangeRates.value.filter((rate) =>
    rate.cur_nm.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

// 통화 선택 옵션
const currencyOptions = computed(() =>
  exchangeRates.value.map((rate) => `${rate.cur_nm} (${rate.cur_unit})`)
);

// 환율 데이터를 가져오는 함수
const fetchExchangeRates = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/exchange/");
    console.log(response.data);
    exchangeRates.value = response.data.map((rate) => ({
      ...rate,
      cur_nm_with_code: `${rate.cur_nm} (${rate.cur_unit})`,
    }));
    console.log(exchangeRates);
    
    // 주요 통화 환율 업데이트
    console.log(exchangeRates.value);
    
    popularCurrencies.value.forEach((currency) => {
      console.log(currency.code);
      const match = exchangeRates.value.find(
        (rate) => rate.cur_unit === currency.code
      );
      if (match) {
        console.log(match.deal_bas_r);
        currency.rate = match.deal_bas_r.replace(",", "");
      }
      else {
        console.log(currency.code);
        
      }
    });
  } catch (error) {
    console.error("환율 데이터를 가져오는 중 오류가 발생했습니다.", error);
  }
};

// 환율 계산 함수
const calculateExchangeRate = () => {
  const baseRate = exchangeRates.value.find(
    (rate) => `${rate.cur_nm} (${rate.cur_unit})` === baseCurrency.value
  );
  const targetRate = exchangeRates.value.find(
    (rate) => `${rate.cur_nm} (${rate.cur_unit})` === targetCurrency.value
  );

  if (baseRate && targetRate && amount.value > 0) {
    const baseToKrw = amount.value * parseFloat(baseRate.deal_bas_r.replace(",", ""));
    const krwToTarget = baseToKrw / parseFloat(targetRate.deal_bas_r.replace(",", ""));
    conversionResult.value = krwToTarget.toFixed(2);
  } else {
    conversionResult.value = null; // 결과 초기화
  }
};

// 값 변경 시 실시간으로 결과 업데이트
watch([baseCurrency, targetCurrency, amount], calculateExchangeRate);

// 데이터 새로고침
const refreshExchangeRates = () => {
  fetchExchangeRates();
};

// 환율 목록 보이기/숨기기
const toggleExchangeList = () => {
  showExchangeList.value = !showExchangeList.value;
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(fetchExchangeRates);
</script>

<style scoped>
h1,
h2 {
  color: #003366;
  font-weight: bold;
}

.v-btn {
  color: white;
}

.v-card {
  width: 200px;
  text-align: center;
}

.d-flex {
  display: flex;
  flex-direction: column; /* 세로 배치를 위한 스타일 */
}

.align-center {
  align-items: center;
}

.result-text {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

img {
  border-radius: 8px;
}
</style>
