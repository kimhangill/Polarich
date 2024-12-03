<template>
    <v-container>
      <v-row class="d-flex justify-center">
        <v-col cols="12" md="8">
          <h2 class="headline">게시글 수정하기</h2>
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
            
            <!-- 기존 이미지 목록 -->
            <div v-if="articleImages.length > 0" class="my-4">
              <h3 class="sub-headline">첨부된 이미지</h3>
              <v-row>
                <v-col
                  v-for="(image, index) in articleImages"
                  :key="index"
                  cols="12"
                  md="4"
                  class="mb-4"
                >
                  <v-card outlined>
                    <v-img :src="image.url" height="150px"></v-img>
                    <v-card-actions class="d-flex justify-end">
                      <v-btn color="red" text @click="removeExistingImage(index)">
                        이미지 삭제
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </div>
  
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
            
            <!-- 수정 완료 및 취소 버튼 -->
            <v-btn color="primary" @click="handleUpdate">수정 완료</v-btn>
            <v-btn color="grey" class="ms-3" @click="handleCancel">취소</v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useRoute, useRouter } from "vue-router";
  import { useArticleStore } from "@/stores/article";
  import Swal from "sweetalert2";
  
  const articleStore = useArticleStore();
  const route = useRoute();
  const router = useRouter();
  
  // 반응형 변수 선언
  const articleTitle = ref("");
  const articleContent = ref("");
  const articleImages = ref([]); // 기존 이미지 목록
  const newImages = ref([]); // 새로 첨부할 이미지 목록
  
  // 유효성 검사 규칙
  const rules = {
    required: value => !!value || "필수 항목입니다.",
  };
  
  // 게시글 정보를 로드하는 함수
  const loadArticleDetail = async () => {
    const id = route.params.id;
    try {
      await articleStore.getArticleDetail(id);
      articleTitle.value = articleStore.articleDetail.title;
      articleContent.value = articleStore.articleDetail.content;
      articleImages.value = articleStore.articleDetail.images; // 기존 이미지 로드
    } catch (error) {
      Swal.fire("에러", "게시글 정보를 불러오는 도중 오류가 발생했습니다.", "error");
    }
  };
  
  // 기존 이미지 삭제 함수
  const removeExistingImage = (index) => {
    articleImages.value.splice(index, 1); // 해당 이미지 삭제
  };
  
  // 수정 완료 버튼 클릭 핸들러
  const handleUpdate = async () => {
  const id = route.params.id;

  // FormData 객체 생성
  const payload = new FormData();

  // 제목과 내용 추가
  payload.append("title", articleTitle.value);
  payload.append("content", articleContent.value);

  // 기존 이미지 ID 추가
  articleImages.value.forEach((image) => {
    payload.append("existing_images", image.id);  // 기존 이미지의 id 전달
  });

  // 새로 추가된 이미지 파일 추가
  newImages.value.forEach((image) => {
    payload.append("new_images", image);  // 이미지 파일 객체를 FormData에 추가
  });

  try {
    await articleStore.putArticle(id, payload);
  } catch (error) {
    console.error("Error updating the article:", error);
  }
};


  
  // 취소 버튼 클릭 핸들러
  const handleCancel = () => {
    router.push(`/article/${route.params.id}`);
  };
  
  // 컴포넌트가 마운트될 때 게시글 세부 정보 로드
  onMounted(loadArticleDetail);
  </script>
  
  <style scoped>
  .headline {
    font-weight: bold;
    font-size: 2rem;
    color: #003366; /* 깊이 있는 블루 */
    margin-bottom: 1rem;
  }
  
  .sub-headline {
    font-weight: bold;
    font-size: 1.5rem;
    color: #003366;
    margin-bottom: 0.5rem;
  }
  </style>
  