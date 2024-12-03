<template>
    <h4 class="text-center">권유받으신 대출의 정보를 바탕으로, 폴라리치가 위험을 탐지해볼게요.</h4>
    <v-container>
      <v-form @submit.prevent="handleSubmit">
        <v-text-field v-model="loanName" label="대출 이름" required></v-text-field>
        <v-select
          v-model="recommendationPath"
          :items="recommendationOptions"
          label="권유 경로"
          required
        ></v-select>
        <v-text-field
          v-model.number="interestRate"
          label="금리 (%)"
          type="number"
          required
        ></v-text-field>
        <v-text-field
          v-model.number="limit"
          label="한도 (만원)"
          type="number"
          required
        ></v-text-field>
        <v-text-field
          v-model.number="period"
          label="기간 (일수)"
          type="number"
          required
        ></v-text-field>
        <v-text-field
          v-model.number="amount"
          label="금액 (만원)"
          type="number"
          required
        ></v-text-field>
        <p class="text-blur small text-muted">
          해당 계산 기능은 사용자의 정보를 바탕으로 특정 사기의 조건을 감지하는 기능을 제공하며, 이는 대출의 사기 유무 판정의 절대적인 기준이 될 수 없습니다. 폴라리치는 이를 바탕으로 한 결과에 대해 책임을 지지 않습니다.
        </p>    
        <v-btn type="submit" color="primary">확인</v-btn>
      </v-form>
</v-container>
  </template>
  
  <script setup>
  import { ref,computed } from 'vue';
  import Swal from 'sweetalert2';
  import { useRouter } from 'vue-router';
  import { useLoanStore } from '@/stores/productStores'; // 스토어 경로에 맞게 임포트
  
  const loanName = ref('');
  const recommendationPath = ref('');
  const interestRate = ref(0);
  const limit = ref(0);
  const period = ref(0);
  const amount = ref(0);

  const recommendationOptions = [
    '홈페이지 안내',
    '은행 영업점',
    'SMS',
    '카카오톡'
  ];
  
  const router = useRouter();
  const loanStore = useLoanStore();
  const loansearch = computed(() => loanStore.searchresults);


  const handleSubmit = async () => {
    // 30-50 대출사기 탐지 로직
    if (
      (amount.value >= 20 && amount.value <= 200) && // 금액 예시: 200만원 이하
      (period.value <= 30 && interestRate.value >= 200) // 기간 예시: 30일 이하, 금리 200% 이상
    ) {
      await Swal.fire({
        icon: 'warning',
        title: '30-50 대출사기가 의심됩니다.',
        text: '폴라리치의 칼럼을 통해 관련 내용을 확인하고, 실제 대출 진행에 주의 바랍니다!'
      }).then(() => {
        router.push({ name: 'ArticleDetailView', params: { id: 4 } }); // 관련 칼럼의 주소로 이동
      });
      return;
    }
    // 스미싱 사기 탐지 로직
    const search = await  loanStore.searchProducts(loanName.value);
    if (search.length > 0) {
      Swal.fire({
        icon: 'info',
        title: '알림',
        text: '해당 대출상품은 폴라리치에 존재하는 대출입니다. 상세 상품 정보의 일치 여부를 폴라리치의 안내 페이지를 확인해보세요.'
      }).then(() => {
        router.push({ name: 'LoanProductView', params: {id: search[0].id } });
      });
    } else {
      // 스미싱 의심 조건
      const averageInterestRate = 3.0; // 대한민국 평균 금리 예시
      const averageLimit = 5000; // 대한민국 평균 한도 예시 (만원)
  
      if (
        (recommendationPath.value === 'SMS' || recommendationPath.value === '카카오톡') &&
        (interestRate.value < averageInterestRate || limit.value > averageLimit)
      ) {
        Swal.fire({
          icon: 'error',
          title: '보이스피싱 빙자 스미싱 사기가 의심됩니다.',
          text: '폴라리치의 칼럼을 통해 관련 내용을 확인하고, 실제 대출 진행에 주의 바랍니다!'
        }).then(() => {
          router.push({ name: 'ArticleDetailView', params: { id: 5 } })
        });
      } else {
        Swal.fire({
          icon: 'info',
          title: 'DB 미등록 대출',
          text: `범위 내 조건을 가졌지만, 폴라리치 DB에 존재하지 않는 대출입니다. ${recommendationPath.value}의 공식 경로를 참고해 보세요!`
        });
      }
    }
  };
  </script>
  
  <style scoped>
.text-blur {
  font-size: 0.8rem;
  color: rgba(0, 0, 0, 0.5);
}
  </style>
  