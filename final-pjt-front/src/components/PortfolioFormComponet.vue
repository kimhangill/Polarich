<template>
  <v-form ref="portfolioForm" v-model="isFormValid" lazy-validation>
    <template v-if="currentPage === 1">
      <v-select
        v-model="portfolio.salary_range"
        :items="translatedSalaryRangeOptions"
        label="연봉 범위"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.occupation"
        :items="translatedOccupationOptions"
        label="직업"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.investment_risk_profile"
        :items="translatedInvestmentRiskOptions"
        label="투자 성향"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.financial_goal"
        :items="translatedFinancialGoalOptions"
        label="재무 목표"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>
    </template>

    <template v-if="currentPage === 2">
      <v-select
        v-model="portfolio.experience_years"
        :items="translatedExperienceYearsOptions"
        label="투자 경험"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.preferred_investment_period"
        :items="translatedInvestmentPeriodOptions"
        label="선호하는 투자 기간"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.liquidity_preference"
        :items="translatedLiquidityPreferenceOptions"
        label="유동성 선호 여부"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.risk_tolerance"
        :items="translatedRiskToleranceOptions"
        label="위험 수용도"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>
    </template>

    <template v-if="currentPage === 3">
      <v-select
        v-model="portfolio.monthly_savings"
        :items="translatedMonthlySavingsOptions"
        label="월 저축액"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.debt_ratio"
        :items="translatedDebtRatioOptions"
        label="부채 비율"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>

      <v-select
        v-model="portfolio.preferred_investment_type"
        :items="translatedPreferredInvestmentTypeOptions"
        label="선호하는 투자 유형"
        required
        outlined
        dense
        class="purple-text mt-3"
      ></v-select>
    </template>

    <v-card-actions class="d-flex justify-space-between mt-5 button-container">
      <v-btn v-if="currentPage > 1" @click="currentPage--" color="grey darken-1" class="white--text" style="min-width: 100px;">
        이전
      </v-btn>
      <v-btn v-if="currentPage < totalPages" @click="nextPage" color="deep-purple accent-4" class="white--text" style="min-width: 100px;">
        다음
      </v-btn>
      <v-btn v-if="currentPage === totalPages" @click="submitPortfolio(portfolio)" color="deep-purple accent-4" class="white--text" style="min-width: 100px;">
        제출
      </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';

const props = defineProps({
  portfolio: Object,
  currentPage: Number,
  totalPages: Number,
});

const emit = defineEmits(['submit']);
const isFormValid = ref(false);
const portfolioForm = ref(null);
const currentPage = ref(1); // 현재 페이지 번호
const totalPages = 3; // 전체 페이지 수

const userStore = useUserStore();

const portfolio = ref({
  salary_range: null,
  occupation: null,
  investment_risk_profile: null,
  financial_goal: null,
  experience_years: null,
  preferred_investment_period: null,
  liquidity_preference: null,
  risk_tolerance: null,
  monthly_savings: null,
  debt_ratio: null,
  preferred_investment_type: null,
});

// 원래 옵션 리스트
const salaryRangeOptions = ["below_24m", "24m_to_36m", "36m_to_50m", "50m_to_70m", "70m_to_100m", "above_100m"];
const occupationOptions = ["student", "employee", "self_employed", "retired", "other"];
const investmentRiskOptions = ["conservative", "moderate", "aggressive"];
const financialGoalOptions = ["home", "retirement", "education", "travel", "investment"];
const experienceYearsOptions = ["none", "less_than_1", "1_to_3", "3_to_5", "more_than_5"];
const investmentPeriodOptions = ["short", "medium", "long"];
const liquidityPreferenceOptions = ["high", "low"];
const riskToleranceOptions = ["low", "medium", "high"];
const monthlySavingsOptions = ["below_300", "300_to_500", "500_to_1000", "1000_to_2000", "above_2000"];
const debtRatioOptions = ["below_10", "10_to_30", "30_to_50", "50_to_70", "above_70"];
const preferredInvestmentTypeOptions = ["stocks", "real_estate", "funds", "bonds", "cryptocurrency"];

// 한글로 번역된 옵션 리스트
const translatedSalaryRangeOptions = computed(() => salaryRangeOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedOccupationOptions = computed(() => occupationOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedInvestmentRiskOptions = computed(() => investmentRiskOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedFinancialGoalOptions = computed(() => financialGoalOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedExperienceYearsOptions = computed(() => experienceYearsOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedInvestmentPeriodOptions = computed(() => investmentPeriodOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedLiquidityPreferenceOptions = computed(() => liquidityPreferenceOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedRiskToleranceOptions = computed(() => riskToleranceOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedMonthlySavingsOptions = computed(() => monthlySavingsOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedDebtRatioOptions = computed(() => debtRatioOptions.map(opt => userStore.choicesTranslation[opt] || opt));
const translatedPreferredInvestmentTypeOptions = computed(() => preferredInvestmentTypeOptions.map(opt => userStore.choicesTranslation[opt] || opt));

// 원본 전달용
const submitPortfolio = (portfolio) => {
  const origin = userStore.reversedChoicesTranslation;
  // originalPortfolio 생성
  const originalPortfolio = {};
  for (const key in portfolio) {
    if (portfolio[key] && origin[portfolio[key]]) {
      // 포트폴리오 값이 존재하고, 역 매핑이 가능한 경우만 추가
      originalPortfolio[key] = origin[portfolio[key]];
    }
  }

  console.log(originalPortfolio);
  emit('submit', originalPortfolio);
};


// 다음 페이지로 이동하는 함수
const nextPage = () => {
  if (portfolioForm.value.validate()) {
    currentPage.value++;
  }
};
</script>

<style lang="scss" scoped>
.purple-text .v-select__selections {
  color: #673ab7 !important;
}
.button-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
.v-btn {
  width: auto !important;
  min-width: 100px;
}
</style>
