<template>
  <v-container style="min-height: 100vh;">

        <!-- 검색 필드 -->
        <v-select
        v-model="searchCriteria"
        :items="searchOptions"
        label="검색 기준"
        style="margin-right: 16px; width: 200px;"
      ></v-select>
      <v-text-field
      v-model="search"
      label="검색"
      placeholder="은행 또는 상품 이름을 입력하세요"
      clearable
      style="margin-bottom: 16px;"
    ></v-text-field>
    <v-data-table
      :headers="headers"
      :items="transformedProducts"
      :items-per-page="2000"
      :loading="loading"
      :hide-default-footer="true"
      loading-text="데이터를 불러오는 중입니다..."
      :footer-props="{ itemsPerPage: -1, itemsPerPageOptions: ['전체'], showFirstLastPage: false }"
      style="min-height: 80vh;"
      item-key="id"
      :search="search"
    >
      <!-- Existing favorite button slot -->
      <template v-slot:item.favorite="{ item }">
        <v-btn
          :class="favorites.includes(item.id) ? 'favorite-active' : 'favorite-inactive'"
          icon
          @click="toggleFavorite(item.id)"
        >
          <v-icon>{{ favorites.includes(item.id) ? 'mdi-star' : 'mdi-star-outline' }}</v-icon>
        </v-btn>
      </template>

      <!-- New detail button slot -->
      <template v-slot:item.detail="{ item }">
        <v-btn icon @click="openDetailDialog(item.id)">
          <v-icon>mdi-information</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <!-- Infinite scroll element -->
    <div ref="observerElement" style="height: 1px;"></div>

    <!-- Detail dialog -->
    <v-dialog v-model="showDetailDialog" max-width="600px">
  <v-card>
    <v-card-title class="dialog-title">
      {{ selectedProductDetail?.fin_prdt_nm }}
    </v-card-title>
    <v-card-text>
      <v-row class="product-header">
        <v-col cols="8">
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-barcode</v-icon>
            <span class="title">상품 코드</span>
            <v-spacer></v-spacer>
            <span class="value">{{ selectedProductDetail?.fin_prdt_cd }}</span>
          </div>
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-bank</v-icon>
            <span class="title">은행</span>
            <v-spacer></v-spacer>
            <span class="value">{{ selectedProductDetail?.kor_co_nm }}</span>
          </div>
        </v-col>
        <v-col cols="4" class="text-right">
          <img :src="`../src/assets/bank/${selectedProductDetail?.kor_co_nm}.png`" alt="은행 로고" class="bank-icon">
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col cols="12">
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-account-group</v-icon>
            <span class="title">가입 대상</span>
            <v-spacer></v-spacer>
            <span class="value">{{ selectedProductDetail?.join_member }}</span>
          </div>
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-sign-direction</v-icon>
            <span class="title">가입 방법</span>
            <v-spacer></v-spacer>
            <span class="value">{{ selectedProductDetail?.join_way }}</span>
          </div>
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-star-circle</v-icon>
            <span class="title">우대 조건</span>
            <v-spacer></v-spacer>
            <span class="value long-text">{{ selectedProductDetail?.spcl_cnd }}</span>
          </div>
          <div class="info-row">
            <v-icon color="#003366" class="mr-2">mdi-note</v-icon>
            <span class="title ">기타 사항</span>
            <v-spacer></v-spacer>
            <span class="value long-text">{{ selectedProductDetail?.etc_note }}</span>
          </div>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <p class="details-title"><strong>세부 옵션</strong></p>
      <div v-for="opt in selectedProductDetail.options" class="option-card">
        <v-divider class="option-divider"></v-divider>
        <v-card outlined>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2">mdi-calendar-clock</v-icon>
                  <span class="title">저축 기간</span>
                  <v-spacer></v-spacer>
                  <span class="value">{{ opt.save_trm }}개월</span>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2">mdi-percent</v-icon>
                  <span class="title">금리 유형</span>
                  <v-spacer></v-spacer>
                  <span class="value">{{ opt.intr_rate_type_nm }}</span>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2">mdi-currency-usd</v-icon>
                  <span class="title">금리</span>
                  <v-spacer></v-spacer>
                  <span class="value">{{ opt.intr_rate }}%</span>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="info-row">
                  <v-icon color="#003366" class="mr-2">mdi-currency-usd-circle</v-icon>
                  <span class="title">최고우대금리</span>
                  <v-spacer></v-spacer>
                  <span class="value">{{ opt.intr_rate2 }}%</span>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
      <!-- Options table -->
      <div v-if="selectedProductDetail?.value?.options && selectedProductDetail.value.options.length">
        <h3>옵션</h3>
        <v-data-table
          :items="selectedProductDetail.value.options"
          :headers="optionHeaders"
          hide-default-footer
        ></v-data-table>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="#003366" text @click="showDetailDialog = false">닫기</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useDepositStore, useSavingStore, useLoanStore } from "@/stores/productStores";

const props = defineProps({ storeType: String });

let store;

if (props.storeType === "deposits") {
  store = useDepositStore();
} else if (props.storeType === "savings") {
  store = useSavingStore();
} else {
  store = useLoanStore();
}

const loading = computed(() => store.loading);
const products = computed(() => store.products);
const hasMore = computed(() => store.hasMore);
const favorites = computed(() => store.favorites);

const observerElement = ref(null);
let observer = null;

// New reactive variables for the detail dialog
const showDetailDialog = ref(false);
const selectedProductDetail = ref(null);

// Convert product data for the table
const terms = [1, 3, 6, 12, 24, 36];
const transformedProducts = computed(() => {
  return products.value.map((product) => {
    const termData = {
      "1": null,
      "3": null,
      "6": null,
      "12": null,
      "24": null,
      "36": null,
    };

    if (Array.isArray(product.options)) {
      product.options.forEach((opt) => {
        if (termData[opt.save_trm] !== undefined) {
          termData[opt.save_trm] = opt.intr_rate;
        }
      });
    }

    return {
      ...product,
      ...termData,
    };
  });
});

// Update headers to include the new "Detail" column
const headers = [
  { align: "center", title: "Id", value: "id" },
  { align: "center", title: "상품 코드", value: "fin_prdt_cd" },
  { align: "center", title: "은행", value: "kor_co_nm" },
  { align: "center", title: "상품 이름", value: "fin_prdt_nm" },
  { align: "center", title: "별무리 달기", value: "favorite", sortable: false },
  { align: "center", title: "상세보기", value: "detail", sortable: false },
  { align: "center", title: "1개월 금리", value: "1", sortable: true },
  { align: "center", title: "3개월 금리", value: "3", sortable: true },
  { align: "center", title: "6개월 금리", value: "6", sortable: true },
  { align: "center", title: "12개월 금리", value: "12", sortable: true },
  { align: "center", title: "24개월 금리", value: "24", sortable: true },
  { align: "center", title: "36개월 금리", value: "36", sortable: true },
];

// Headers for the options table in the dialog
const optionHeaders = [
  { text: "금리 유형", value: "intr_rate_type_nm" },
  { text: "저축 기간", value: "save_trm" },
  { text: "금리", value: "intr_rate" },
  { text: "최고 우대금리", value: "intr_rate2" },
];

// Infinite scroll handling
const handleIntersect = (entries) => {
  const [entry] = entries;
  if (entry.isIntersecting && hasMore.value && !loading.value) {
    store.fetchProducts(true);
  }
};
// 서치기능 구현
const search = ref('')
const searchOptions = ref([
      { title: "은행", value: "kor_co_nm" },
      { title: "상품 이름", value: "fin_prdt_nm" },
    ]);
const filteredProducts = computed(() =>
      products.value.filter(
        (product) =>
          product.kor_co_nm.includes(search.value) ||
          product.fin_prdt_nm.includes(search.value)
      )
    );

// Setup the Intersection Observer
onMounted(() => {
  store.fetchProducts();

  observer = new IntersectionObserver(handleIntersect, {
    root: null,
    threshold: 1.0,
  });

  if (observerElement.value) {
    observer.observe(observerElement.value);
  }
});

onUnmounted(() => {
  if (observer && observerElement.value) {
    observer.unobserve(observerElement.value);
  }
});

// Method to toggle favorites
const toggleFavorite = (productId) => {
  store.addFavorite(productId);
};

// Method to open the detail dialog
const openDetailDialog = async (productId) => {
  selectedProductDetail.value = await store.fetchProductDetail(productId);
  console.log(selectedProductDetail.value);

  showDetailDialog.value = true;
};

// Watcher to reset selected product detail when the dialog closes
// watch(showDetailDialog, (newVal) => {
//   if (!newVal) {
//     selectedProductDetail.value = null;
//   }
// });
</script>

<style scoped>
.favorite-active {
  background-color: #001f3f;
  color: #FFD700;
  transition: all 0.3s ease;
}

.favorite-inactive {
  color: #808080;
}

.text-center {
  text-align: center;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #003366; /* 어두운 블루 색상 */
  border-bottom: 2px solid #f5c242; /* 골드 색상으로 하단 테두리 추가 */
  padding-bottom: 0.5rem;
}

.dialog-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: #003366;
  border-bottom: 1px solid #f5c242;
  padding-bottom: 0.5rem;
}

.long-text {
  display: block;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 100px;
  overflow: auto;
  padding: 0.5rem;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.option-item {
  margin-bottom: 1rem;
}

.info-title {
  font-weight: bold;
  color: #555;
  margin-right: 5px;
}

.info-value {
  color: #333;
}

.product-header {
  margin-bottom: 10px;
}

.details-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-top: 20px;
}

.bank-icon {
  width: 100px;
  height: auto;
}

.long-text {
  display: inline-block;
  max-width: 100%;
  white-space: pre-wrap;
  word-break: break-word;
}

.option-card {
  margin-top: 15px;
}

.option-divider {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
