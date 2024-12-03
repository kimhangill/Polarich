<template>
  <v-container>
    <v-row class="d-flex justify-center">
      <v-col cols="12" md="8">
        <h2 class="headline">새 게시글 작성하기</h2>
        <v-form ref="form">
          <!-- 제목 입력 필드 -->
          <v-text-field
            label="제목"
            v-model="articleTitle"
            :rules="[rules.required]"
            outlined
          ></v-text-field>

          <!-- 내용 입력 필드 -->
          <v-textarea
            label="내용"
            v-model="articleContent"
            :rules="[rules.required]"
            outlined
            rows="10"
          ></v-textarea>

          <!-- 타입 선택 필드 -->
          <v-select
            label="게시글 타입"
            v-model="articleType"
            :items="articleTypes"
            :rules="[rules.required, rules.checkColumnPermission]"
            outlined
          ></v-select>

          <!-- 이미지 첨부 필드 -->
          <v-file-input
            label="이미지 첨부 (여러 개 선택 가능)"
            v-model="newImages"
            multiple
            show-size
            accept="image/*"
            prepend-icon="mdi-image"
          ></v-file-input>

          <v-divider class="my-4"></v-divider>

          <!-- 작성 완료 및 취소 버튼 -->
          <v-btn
            color="primary"
            @click="handleCreate"
            :disabled="!canCreateColumn && articleType === 'column'"
          >작성 완료</v-btn>
          <v-btn color="grey" @click="handleCancel">취소</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useArticleStore } from "@/stores/article";
import { useUserStore } from "@/stores/user";
import Swal from "sweetalert2";

const articleStore = useArticleStore();
const userStore = useUserStore();
const router = useRouter();

// 반응형 변수 선언
const articleTitle = ref("");
const articleContent = ref("");
const articleType = ref(""); // 게시글 타입
const newImages = ref([]); // 새로 첨부할 이미지 목록

// 타입 선택 옵션
const articleTypes = ["general", "column", "qna"];

// 로그인된 사용자가 `column` 타입 게시글을 작성할 수 있는지 확인
const canCreateColumn = computed(() => {
  return userStore.userProfile?.isProfessional || false;
});

// 유효성 검사 규칙
const rules = {
  required: value => !!value || "필수 항목입니다.",
  // column 타입에 대한 작성 권한 검사
  checkColumnPermission: value => {
    if (value === "column" && !canCreateColumn.value) {
      return "프로페셔널 사용자만 작성할 수 있습니다.";
    }
    return true;
  },
};



// 작성 완료 버튼 클릭 핸들러
const handleCreate = async () => {
  const payload = new FormData();
  payload.append("title", articleTitle.value);
  payload.append("content", articleContent.value);
  payload.append("type", articleType.value); // 타입 추가

  // 새로 첨부된 이미지 파일 추가
  newImages.value.forEach((image) => {
    payload.append("new_images", image);
  });
  await articleStore.postArticle(payload);
};

// 취소 버튼 클릭 핸들러
const handleCancel = () => {
  router.back();
};
</script>

<style scoped>
.headline {
  font-weight: bold;
  font-size: 2rem;
  color: #003366;
  margin-bottom: 1rem;
}
</style>
