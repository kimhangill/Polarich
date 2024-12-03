<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h3>댓글</h3>
      </v-col>
    </v-row>

    <v-row v-for="comment in comments" :key="comment.id" class="answer-item">
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-text>
            <div class="answer-header">
              <v-avatar>
                  <img :src="fullImageUrl(comment.user_profileImage)" alt="프로필 이미지" width="100%" height="100%">
              </v-avatar>
              <span class="answer-username">{{ comment.user_nickname }}</span>
            </div>
            <div v-if="editingCommentId !== comment.id" class="answer-content">
              {{ comment.content }}
            </div>
            <div v-else>
              <v-textarea v-model="editedCommentContent" label="댓글 수정" outlined></v-textarea>
              <v-btn color="primary" @click="updateComment(comment.id)">수정</v-btn>
              <v-btn color="red" text @click="cancelEdit">수정 취소</v-btn>
            </div>

            <v-btn
              v-if="isAuthor(comment) && editingCommentId !== comment.id"
              color="primary"
              text
              @click="editComment(comment)"
            >
              수정
            </v-btn>
            <v-btn
              v-if="isAuthor(comment) && editingCommentId !== comment.id"
              color="red"
              text
              @click="deleteComment(comment.id)"
            >
              삭제
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 답변 작성 폼 (프로페셔널 유저만 보임) -->
    <v-row v-if="userStore.userProfile">
      <v-col cols="12">
        <v-form>
          <v-textarea
            v-model="newCommentContent"
            label="댓글 작성"
            outlined
          ></v-textarea>
          <v-btn color="primary" @click="postComment">댓글 작성</v-btn>
        </v-form>
      </v-col>
    </v-row>
    <v-btn color="secondary" text @click="router.back()">돌아가기</v-btn>
  </v-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useCommentStore } from '@/stores/comment';
import { defineProps } from 'vue';
import Swal from 'sweetalert2';
import router from '@/router';
const props = defineProps({
  articleId: Number,
});

const userStore = useUserStore();
const commentStore = useCommentStore();
const newCommentContent = ref('');
const editedCommentContent = ref('');
const editingCommentId = ref(null);
const isAuthenticated = computed(() => userStore.userProfile);
const baseURL = "http://127.0.0.1:8000";

  const fullImageUrl = (path) => {
  return baseURL + path;
  };
// 답변 작성자 확인 함수
const isAuthor = (comment) => {
  return userStore.userProfile && userStore.userProfile.id === comment.user;
};

// 답변 작성 함수
const postComment = async () => {
  if (newCommentContent.value.trim() !== '') {
    try {
      const payload = { article:props.articleId, content: newCommentContent.value }
      console.log(payload);
      await commentStore.postComment(payload);
      newCommentContent.value = '';
      await refreshComments(); // 답변 작성 후 목록 갱신
    } catch (error) {
      console.error('댓글 작성 중 오류 발생:', error);
    }
  }
};

const comments = computed(() => commentStore.comments);

// 답변 목록 갱신 함수
const refreshComments = async () => {
  try {
    await commentStore.getComment(props.articleId);
    console.log(comments.value);
    
  } catch (error) {
    console.error('댓글 목록을 갱신하는 중 오류 발생:', error);
  }
};

// 답변 수정 함수
const editComment = (comment) => {
  editingCommentId.value = comment.id;
  editedCommentContent.value = comment.content;
};

const cancelEdit = () => {
  editingCommentId.value = null;
  editedCommentContent.value = '';
};

const updateComment = async (commentId) => {
  if (editedCommentContent.value.trim() !== '') {
    try {
      await commentStore.putComment(commentId, { id: commentId, article: props.articleId, content: editedCommentContent.value });
      editingCommentId.value = null;
      editedCommentContent.value = '';
      await refreshComments();
    } catch (error) {
      console.error('댓글 수정 중 오류 발생:', error);
    }
  }
};

// 답변 삭제 함수
const deleteComment = async (commentId) => {
  try {
    const result = await Swal.fire({
      title: '정말 댓글을 삭제하시겠습니까?',
      text: '이 작업은 되돌릴 수 없습니다.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '삭제',
      cancelButtonText: '취소'
    });

    if (result.isConfirmed) {
      await commentStore.deleteComment(commentId);
      await refreshComments();
    }
  } catch (error) {
    console.error('댓글 삭제 중 오류 발생:', error);
  }
};

onMounted(() => commentStore.getComment(props.articleId));
</script>

<style scoped>
.answer-item {
  margin-bottom: 2rem;
}
.answer-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.answer-username {
  margin-left: 1rem;
  font-weight: bold;
}
.answer-content {
  font-size: 1.2rem;
}
</style>
