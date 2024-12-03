<template>
    <div>
      <!-- 게시글 목록 -->
      <div class="articles-section">
        <h3 class="section-title mt-3">작성한 글 목록</h3>
        <v-data-table
          :items="userArticles"
          :headers="articleHeaders"
          class="elevation-1 clickable-table"
          v-if="!isLoadingArticles"
          @click:row="gotoArticleDetailPage"
        >
          <template #item="{ item }">
            <tr @click="gotoArticleDetailPage(item.id)" class="clickable-row">
              <td class="title-cell">{{ item.title }}</td>
              <td class="date-cell">{{ item.created_at.slice(0, 10) }}</td>
              <td class="comment-count-cell">
                <v-chip color="primary" outlined>{{ item.comment_count }}</v-chip>
              </td>
            </tr>
          </template>
        </v-data-table>
        <div v-else>로딩 중입니다...</div>
      </div>
  
      <!-- 댓글 목록 -->
      <div class="comments-section">
        <h3 class="section-title">작성한 댓글 목록</h3>
        <v-row  v-for="comment in userComments" :key="comment.id" class="comment-item">
          <v-col cols="12">
            <v-card class="mb-2">
              <v-card-text>
                <div class="comment-header">
                  <span class="comment-username">{{ comment.user_nickname }}</span>
                  <span class="comment-id">{{ comment.created_at.slice(0, 10) }}</span>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <v-btn color="primary" text @click="gotoArticleDetailPage(comment.article)">
                  게시글로 이동
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useArticleStore } from '@/stores/article';
  import { useCommentStore } from '@/stores/comment';
  import { useRoute, useRouter } from 'vue-router';
  import { useUserStore } from '@/stores/user';
  
  const articleStore = useArticleStore();
  const commentStore = useCommentStore();
  const route = useRoute();
  const router = useRouter();
  const userStore = useUserStore();
  const userArticles = computed(() => articleStore.userArticles);
  const userComments = computed(() => commentStore.userComments);
  const isLoadingComments = ref(true)
  const isLoadingArticles = ref(true)
  // 테이블 헤더 정의
  const articleHeaders = [
    { title: '제목', value: 'title' },
    { title: '작성일', value: 'created_at', sortable: true },
    { title: '댓글 수', value: 'comment_count', sortable: true }
  ];
  
  // 게시글 및 댓글 데이터 가져오기
  onMounted(async () => {
  const username = userStore.userProfile.username;
  await articleStore.getArticleByUser(username);
  isLoadingArticles.value = false;
  
  await commentStore.getCommentByUser(username);
  isLoadingComments.value = false;
});
  // 게시글 상세 보기로 이동
  const gotoArticleDetailPage = (item) => {
    if (item) {
      router.push({ name: 'ArticleDetailView', params: { id: item } });
    }
  };
  </script>
  
  <style scoped>
  .clickable-table .clickable-row:hover {
    background-color: rgba(0, 51, 102, 0.1);
    cursor: pointer;
  }
  
  .comment-item {
    margin-bottom: 1rem; /* 댓글 상자 간 마진 줄이기 */
  }
  
  .articles-section, .comments-section {
    margin-bottom: 3rem;
  }
  
  .section-title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #003366; /* 어두운 블루 색상 */
    border-bottom: 2px solid #f5c242; /* 골드 색상으로 하단 테두리 추가 */
    padding-bottom: 0.5rem;
  }
  
  .comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem; /* 마진을 줄여서 간격을 조정 */
  }
  
  .comment-username {
    font-weight: bold;
  }
  
  .comment-date {
    color: #888;
  }
  
  .comment-content {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  </style>
  