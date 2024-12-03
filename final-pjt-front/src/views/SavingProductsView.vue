<template>
  <div>
    <h1 class="section-title">적금 상품 리스트</h1>
    <ProductList storeType="savings" /> <!-- storeType을 "deposit"으로 설정 -->
  </div>
</template>

<script>
import ProductList from '@/components/ProductList.vue';

export default {
  components: {
    ProductList,
  },
};
</script>
