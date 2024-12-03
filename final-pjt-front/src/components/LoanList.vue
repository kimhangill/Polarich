<template>
    <v-divider></v-divider>
    <v-container>
      <!-- 로딩 중 메시지 -->
      <v-row v-if="isLoading" justify="center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-row>
  
      <!-- 게시글 목록 (테이블 형태) -->
      <v-row v-else>
        <!-- 검색 필드 및 검색 기준 선택 -->
        <v-row align="center" style="margin-bottom: 16px;">
          <!-- 검색 기준 선택 -->
          <v-col cols="2">
            <v-select
              v-model="searchCriteria"
              :items="searchOptions"
              label="검색 기준"
              dense
              outlined
            ></v-select>
          </v-col>
          <!-- 검색 입력 -->
          <v-col cols="10">
            <v-text-field
              v-model="search"
              label="검색"
              placeholder="검색어를 입력하세요"
              clearable
              dense
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-col cols="12">
            <v-alert type="warning" border="left" color="#ffcc00" text>
    온라인 금융플랫폼에서 제공하는 대출상품의 비교 및 추천 서비스는 금융소비자보호법 제11조 및 제24조에 따라 금융상품판매업자로 등록되지 않은 자가 수행할 수 없음을 안내드립니다.
            </v-alert>

          <v-data-table
            :items="filteredProducts"
            :headers="headers"
            class="elevation-1 clickable-table"
            @click:row="gotoDetailPage"
            item-class="product-row"
          >
            <template #item="{ item }">
              <tr @click="gotoDetailPage(item)" class="clickable-row">
                <td class="id-cell">{{ item.id }}</td>
                <td class="code-cell">{{ item.fin_prdt_cd }}</td>
                <td class="bank-cell">{{ item.kor_co_nm }}</td>
                <td class="name-cell">{{ item.fin_prdt_nm }}</td>
                <td class="type-cell">{{ item.crdt_prdt_type_nm }}</td>
                <td class="join-way-cell">{{ item.join_way }}</td>
              </tr>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
  
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from "vue";
  import { useLoanStore } from "@/stores/productStores";
  import router from "@/router";
  import { useRoute } from "vue-router";
  
  const props = defineProps(["type"]);
  const creditLoanStore = useLoanStore();

  
  // 검색 필드와 상태
  const search = ref(""); // 검색어
  const searchCriteria = ref("fin_prdt_nm"); // 기본 검색 기준은 "상품 이름"
  const searchOptions = ref([
    { title: "상품 이름", value: "fin_prdt_nm" },
    { title: "은행", value: "kor_co_nm" },
  ]);
  const products = ref([]); // 상품 리스트
  const isLoading = ref(true); // 로딩 상태
  
  // 테이블 헤더 정의
  const headers = [
    { title: "ID", value: "id" },
    { title: "상품 코드", value: "fin_prdt_cd" },
    { title: "은행", value: "kor_co_nm" },
    { title: "상품 이름", value: "fin_prdt_nm" },
    { title: "상품 유형", value: "crdt_prdt_type_nm" },
    { title: "가입 방법", value: "join_way" },
  ];
  
  // 상품 리스트를 가져온 후 데이터 포맷팅
  const fetchProducts = async () => {
    try {
      await creditLoanStore.fetchProducts(props.type)
      products.value = creditLoanStore.products;
    } catch (error) {
      console.error("상품 목록을 가져오는 중 문제가 발생했습니다.", error);
    } finally {
      isLoading.value = false;
    }
  };
  
  // 검색된 상품 계산
  const filteredProducts = computed(() =>
    products.value.filter((product) =>
      product[searchCriteria.value]?.includes(search.value)
    )
  );
  
  // 글쓰기 페이지 이동
  const gotoWrite = () => {
    router.push({ name: "CreateCreditLoanView" });
  };
  
  // 상품 상세 페이지 이동
  const gotoDetailPage = (item) => {
    if (item) {
      router.push({ name: "LoanProductView", params: { id: item.id } });
    }
  };
  
  // 컴포넌트 마운트 시 상품 가져오기
  onMounted(() => {
    fetchProducts();
  });
  
  const route = useRoute();
  watch(
    () => route.params.type,
    (newType) => {
      fetchProducts(newType);
    }
  );
  </script>
  
  <style>
  /* 기존 스타일 유지 */
  .clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background-color: #f5f5f5; /* 호버 시 배경색 변경 */
}
  </style>
  