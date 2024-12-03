<template>
  <v-container>
    <!-- 로딩 중 메시지 -->
    <v-row v-if="isLoading" justify="center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </v-row>

    <!-- 상세 정보 컴포넌트 -->
    <template v-else-if="articleDetail">
      <ArticleDetailComponent :article="articleDetail" />

      <!-- 댓글 컴포넌트 또는 Q&A 컴포넌트 -->
      <template v-if="articleDetail.type === 'qna'">
        <QnAcomponent :article-id="articleDetail.id" :comments="articleDetail?.comments" />
      </template>
      <template v-else>
        <CommentsComponent :comments="articleDetail?.comments" :article-id="articleDetail.id" />
      </template>
    </template>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useArticleStore } from "@/stores/article";
import ArticleDetailComponent from "@/components/ArticleDetailComponent.vue";
import CommentsComponent from "@/components/CommentsComponent.vue";
import QnAcomponent from "@/components/QnAcomponent.vue";
import { LogarithmicScale } from "chart.js";

// 반응형 변수 선언
const article = ref(null);
const isLoading = ref(true); // 로딩 상태 추가
const route = useRoute();
const articleStore = useArticleStore(); // ArticleStore 가져오기
const articleDetail = computed(() => articleStore.articleDetail);
// 게시글 상세 정보를 가져오는 함수

const fetchArticleDetail = async () => {
  const id = route.params.id; // 라우터에서 ID 가져오기
  try {
    article.value = await articleStore.getArticleDetail(id); // ArticleStore에서 세부 정보 가져오기
  } catch (error) {
    console.error("게시글 정보를 가져오는 중 오류 발생:", error);
  } finally {
    isLoading.value = false; // 데이터 로드 완료 후 로딩 상태 변경
  }
};

// 컴포넌트가 마운트될 때 게시글 상세 정보 가져오기
onMounted(fetchArticleDetail);
console.log(article.value);

</script>
