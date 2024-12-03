<template>
    <div>
      <h1 class="section-title">"{{ keyword }}" 의 통합검색 결과입니다.</h1>
  
      <h3 class="section-title">금융 상품</h3>
      <h4>예금</h4>
      <template v-if="depositSearch.length">
        <v-list>
          <v-list-item v-for="deposit in depositSearch" :key="deposit.id" class="mb-2">
            <v-list-item-content>
              <v-list-item-title>상품명: {{ deposit.fin_prdt_nm }}</v-list-item-title>
              <v-list-item-subtitle>{{ deposit.kor_co_nm }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="primary" @click="moveproduct('deposit', deposit.id)" small>바로가기</v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-divider></v-divider>
        </v-list>
      </template>
      <v-alert type="info" v-else>검색 결과가 존재하지 않습니다!</v-alert>
  
      <h4>적금</h4>
      <template v-if="savingSearch.length">
        <v-list>
          <v-list-item v-for="saving in savingSearch" :key="saving.id" class="mb-2">
            <v-list-item-content>
              <v-list-item-title>상품명: {{ saving.fin_prdt_nm }}</v-list-item-title>
              <v-list-item-subtitle>{{ saving.kor_co_nm }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="success" @click="moveproduct('saving', saving.id)" small>바로가기</v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-divider></v-divider>
        </v-list>
      </template>
      <v-alert type="info" v-else>검색 결과가 존재하지 않습니다!</v-alert>
  
      <h3 class="section-title">게시글</h3>
      
      <template v-if="articleSearch.length">
        <v-list>
          <v-list-item v-for="article in articleSearch" :key="article.id" class="mb-2">
            <v-list-item-content>
              <v-list-item-title>{{ article.title }} </v-list-item-title>
              <v-list-item-subtitle>
                작성자: {{ article.user_nickname }} | 작성일: {{ article.created_at.slice(0, 10) }} | {{ typeTranse[article.type] }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="info" @click="movearticle(article.id)" small>바로가기</v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-divider></v-divider>
        </v-list>
      </template>
      <v-alert type="info" v-else>검색 결과가 존재하지 않습니다!</v-alert>
    </div>
  </template>
  
  
  <script setup>
  import { onMounted, ref,computed,onBeforeUnmount,watch  } from 'vue';
  import { useRoute } from 'vue-router';
  import { useDepositStore, useSavingStore } from '@/stores/productStores';
  import { useArticleStore } from '@/stores/article';
  import ProductDetailView from './ProductDetailView.vue';
  import ArticleDetailView from './ArticleDetailView.vue';
  import router from '@/router';
  const typeTranse = {'qna':'QnA게시판','general':'자유','column':'칼럼'}
  const moveproduct = function (type, id) {
    router.push({name:"ProductDetailView", params:{type:type,id:id}})
  }
  const movearticle = function (id) {
    router.push({ name: "ArticleDetailView", params: { id:id } });
  }
  const route = useRoute()
  const keyword = ref(route.query.q)
  const depositStore = useDepositStore()
  const savingStore = useSavingStore()
  const articleStore = useArticleStore()
  const depositSearch = computed(() => depositStore.searchresults);
  const savingSearch = computed(() => savingStore.searchresults);
  const articleSearch = computed(()=> articleStore.searchresults)


  // 라이프사이클 훅
  onMounted(()=>{
    depositStore.searchProducts(keyword.value)
    savingStore.searchProducts(keyword.value)
    articleStore.searchgetArticleList(keyword.value)
  })

  watch(
  () => route.query.q,
  (newQuery, oldQuery) => {
    if (newQuery !== oldQuery) {
      // 새로운 검색어로 데이터 다시 로드
      depositStore.searchProducts(newQuery)
      savingStore.searchProducts(newQuery)
      articleStore.searchgetArticleList(newQuery)
      keyword.value=newQuery
    }
  }
)

  onBeforeUnmount(() => {
  depositStore.searchresults = [];
  savingStore.searchresults = [];
  articleStore.searchresults = [];
});
  </script>