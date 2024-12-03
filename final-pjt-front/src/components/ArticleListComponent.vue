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
        <v-data-table
          :items="filteredArticles"
          :headers="headers"
          class="elevation-1 clickable-table"
          @click:row="gotoDetailPage"
          item-class="article-row"
        >
          <template #item="{ item }">
            <tr @click="gotoDetailPage(item)" class="clickable-row">
              <td class="title-cell">{{ item.title }}</td>
              <td class="author-cell">{{ item.user_nickname }}</td>
              <td class="date-cell">{{ item.created_at }}</td>
              <td class="comment-count-cell">
                <v-chip color="primary" outlined class="comment-chip-left">{{ item.comment_count }}</v-chip>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- 글쓰기 버튼 -->
    <v-btn @click="gotoWrite" class="write-button" color="#f5c242" dark fab>
      <v-icon>mdi-pencil</v-icon>
    </v-btn>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useArticleStore } from "@/stores/article";
import router from "@/router";
import { useRoute } from "vue-router";

const props = defineProps(["type"]);
const articleStore = useArticleStore();
const { getArticleList } = articleStore;

// 검색 필드와 상태
const search = ref(""); // 검색어
const searchCriteria = ref("title"); // 기본 검색 기준은 "title"
const searchOptions = ref([
  { title: "글 제목", value: "title" },
  { title: "작성자 닉네임", value: "user_nickname" },
]);
const articles = ref([]); // 게시글 리스트
const isLoading = ref(true); // 로딩 상태

// 테이블 헤더 정의
const headers = [
  { title: "제목", value: "title" },
  { title: "작성자", value: "user_nickname" },
  { title: "작성일", value: "created_at", sortable: true },
  { title: "댓글 수", value: "comment_count", sortable: true },
];

// 게시글 리스트를 가져온 후 데이터 포맷팅
const fetchArticles = async () => {
  try {
    await getArticleList(props.type);
    articles.value = articleStore.articlesList.map((article) => ({
      ...article,
      created_at: article.created_at.slice(0, 10), // YYYY-MM-DD만 추출
    }));
  } catch (error) {
    console.error("게시글 목록을 가져오는 중 문제가 발생했습니다.", error);
  } finally {
    isLoading.value = false;
  }
};

// 검색된 게시글 계산
const filteredArticles = computed(() =>
  articles.value.filter((article) =>
    article[searchCriteria.value]?.includes(search.value)
  )
);

// 글쓰기 페이지 이동
const gotoWrite = () => {
  router.push({ name: "CreateArticleView" });
};

// 게시글 상세 페이지 이동
const gotoDetailPage = (item) => {
  if (item) {
    router.push({ name: "ArticleDetailView", params: { id: item.id } });
  }
};

// 컴포넌트 마운트 시 게시글 가져오기
onMounted(() => {
  fetchArticles();
});

const route = useRoute();
watch(
  () => route.params.type,
  (newType) => {
    fetchArticles(newType);
  }
);
</script>

<style>
/* 기존 스타일 유지 */
</style>
