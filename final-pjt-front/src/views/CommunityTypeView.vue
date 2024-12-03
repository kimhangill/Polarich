<template>
    <div>
      <h1 class="section-title">{{ viewTitle }}</h1>
      <ArticleListComponent
        v-if="!isDetailView"
        :type="type"
        @selectArticle="openDetail"
      />
      <ArticleDetailComponent
        v-else
        :articleId="selectedArticleId"
        @backToList="closeDetail"
      />
    </div>
  </template>
  
  <script>
  import { reactive, computed } from "vue";
  import { useRoute } from "vue-router";
  import ArticleListComponent from "@/components/ArticleListComponent.vue";
  import ArticleDetailComponent from "@/components/ArticleDetailComponent.vue";
  
  export default {
    components: { ArticleListComponent, ArticleDetailComponent },
    setup() {
      const state = reactive({
        isDetailView: false,
        selectedArticleId: null,
      });
  
      const route = useRoute();
      const type = computed(() => route.params.type || "general");
  
      const viewTitle = computed(() => {
        switch (type.value) {
          case "general":
            return "자유 게시판";
          case "column":
            return "칼럼 게시판";
          case "qna":
            return "Q&A 게시판";
          default:
            return "커뮤니티";
        }
      });
  
      const openDetail = (articleId) => {
        state.selectedArticleId = articleId;
        state.isDetailView = true;
      };
  
      const closeDetail = () => {
        state.selectedArticleId = null;
        state.isDetailView = false;
      };
  
      return {
        type,
        viewTitle,
        ...state,
        openDetail,
        closeDetail,
      };
    },
  };
  </script>
  