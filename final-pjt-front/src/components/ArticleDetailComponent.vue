<template>
  <v-container>
    <!-- 제목 -->
    <v-row>
      <v-col>
        <h1 class="section-title">{{ props.article.title }}</h1>
      </v-col>
    </v-row>

    <!-- 작성자와 글번호 정보 -->
    <v-row class="article-info-row">
      <v-col cols="12" md="6">
        <span class="article-info">작성자: {{ props.article.user_nickname }}</span>
      </v-col>
      <v-col cols="12" md="6" class="text-md-right">
        <span class="article-info">글번호: {{ props.article.id }}</span>
      </v-col>
    </v-row>

    <v-divider></v-divider>

        <!-- 이미지 목록 -->
        <v-row class="image-list-row" v-if="props.article.images.length > 0">
      <v-col
        v-for="(image, index) in props.article.images"
        :key="index"
        cols="12"
        md="4"
        class="mb-4"
      >
        <v-img
          :src="image.image"
          class="clickable-image"
          @click="openImagePopup(image.image)"
          height="150"
          contain
        ></v-img>
      </v-col>
    </v-row>

    <v-divider></v-divider>
    <!-- 본문 내용 -->
    <v-row>
      <v-col>
        <div class="body-text">
          <p v-html="renderMarkdown(props.article?.content)"></p>
        </div>
      </v-col>
    </v-row>



    <!-- 수정 및 삭제 버튼 -->
    <v-row v-if="isAuthor">
      <v-col class="d-flex justify-end">
        <v-btn color="primary" text @click="handleEdit">수정하기</v-btn>
        <v-btn color="red" text @click="handleDelete">삭제하기</v-btn>
      </v-col>

    </v-row>
    

    <!-- 이미지 확대 팝업 -->
    <v-dialog v-model="imageDialog" max-width="800">
      <v-card>
        <v-img :src="selectedImage" height="500"></v-img>
        <v-card-actions>
          <v-btn color="primary" text @click="imageDialog = false">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { defineProps, ref, computed } from "vue";
import { useArticleStore } from "@/stores/article";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";
import { marked } from 'marked';

const renderMarkdown = (content) => {
  return marked(content);
  };
const props = defineProps({
  article: Object,
});

// Article Store 및 Router 가져오기
const articleStore = useArticleStore();
const userStore = useUserStore();
const router = useRouter();

// 로그인된 사용자가 작성자인지 확인하는 계산된 속성
const isAuthor = computed(() => {
  console.log(props.article.user.id);
  return userStore.userProfile?.id === props.article.user;
});

// 이미지 확대 팝업 상태 및 선택된 이미지
const imageDialog = ref(false);
const selectedImage = ref("");

// 이미지 확대 팝업 열기
const openImagePopup = (imageUrl) => {
  selectedImage.value = imageUrl;
  imageDialog.value = true;
};

// 수정하기 함수
const handleEdit = () => {
  const id = props.article.id;
  router.push({ name: "EditArticleView", params: { id } });
};

// 삭제하기 함수
const handleDelete = async () => {
  try {
    await articleStore.deleteArticle(props.article.id,props.article.type);
  } catch (error) {
    Swal.fire("에러", "게시글 삭제 중 문제가 발생했습니다.", "error");
  }
};
</script>

<style scoped>
.headline {
  font-weight: bold;
  font-size: 2.5rem;
  color: #003366;
  margin-bottom: 0.5rem;
}

.article-info-row {
  margin-bottom: 1rem;
}

.article-info {
  font-size: 1rem;
  color: #555;
}

.body-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
}

.image-list-row {
  margin-top: 1.5rem;
}

.clickable-image {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.clickable-image:hover {
  transform: scale(1.05);
}

.v-btn {
  margin-left: 8px;
}
</style>
