<template class="bg">
  <v-container class="login-form">
     <!-- 로그인 카드 -->
    <v-card class="mx-auto pa-8 pt-10 pb-4 bg-image " elevation="4" max-width="448" rounded="lg" style="margin-top: 60px;">
      <!-- 상단 이모티콘 -->
      <v-row justify="center" class="mb-6" style="margin-bottom: 20px;">
        <div style="width: 170px; height: 100px; overflow: hidden; border-radius: 8px;">
          <img :src="imagePath" alt="프로필 이미지" style="object-fit: cover; width: 100%; height: 100%;" />
        </div>
      </v-row>
      <!-- 로그인 폼 -->
      <v-form @submit.prevent="submitForm">
        <!-- 아이디 -->
        <div 
          class="text-subtitle-1 custom-white-text text-medium-emphasis"
        >
          아이디
        </div>

        <v-text-field
          class="text-field-custom"
          v-model="state.username"
          @blur="v$.username.$touch"
          density="compact"
          placeholder="아이디 또는 전화번호"
          prepend-inner-icon="mdi-information"
          variant="outlined"
        ></v-text-field>

        <!-- 비밀번호 -->
        <div 
          class="text-subtitle-1 custom-white-text text-medium-emphasis d-flex align-center justify-space-between"
        >
          비밀번호
        </div>

        <v-text-field
          class="text-field-custom"
          v-model="state.password"
          @blur="v$.password.$touch"
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          density="compact"
          placeholder="비밀번호"
          prepend-inner-icon="mdi-lock-outline"
          variant="outlined"
          @click:append-inner="visible = !visible"
        ></v-text-field>

        <!-- 로그인 버튼 -->
        <v-card-actions class="justify-center mt-8">
          <v-btn
            type="submit"
            class="mb-4 button-custom"
            size="large"
            variant="tonal"
            block
          >
            로그인
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import useVuelidate from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { useUserStore } from "@/stores/user";
import swal  from "sweetalert";
const visible = ref(false);
const imagePath = "src/assets/logo.png";

const userStore = useUserStore();
// 상태 정의
const state = ref({
  username: "",
  password: "",
});

// 유효성 검사 규칙 정의
const rules = {
  username: { required, maxLength: maxLength(20) },
  password: { required, maxLength: maxLength(128) },
};

// Vuelidate 훅 사용
const v$ = useVuelidate(rules, state);

function submitForm() {
  v$.value.$validate();
  if (!v$.value.$error) {
    // 유효성 검사를 통과한 경우 처리 로직
    const payload = {
      username: state.value.username,
      password: state.value.password,
    };
    userStore.login(payload);
  } else {
    // 유효성 검사를 통과하지 못한 경우 처리 로직
    swal({title:'폼을 확인해주세요'})
  }
}
</script>

<style>
.bg {
  background-image: url('@/assets/bgbg1.png'); /* 배경 이미지 경로 */
}
.button-custom {
  background-color: blue !important; /* 버튼 배경색 파란색 */
  color: rgb(252, 247, 247) !important;         /* 버튼 텍스트 하얀색 */
  border-radius: 8px;              /* 버튼 모서리 둥글게 */
}
.bg-image {
  background-color: rgba(255, 255, 255, 0.6); /* 반투명 흰색 배경 */
  backdrop-filter: blur(10px); /* 블러 효과 */
  background-size: cover;
  background-position: center;  
  background-repeat: no-repeat;
}
.text-field-custom .v-input {
  border: 1px solid rgb(19, 18, 18) !important; /* 테두리를 하얗게 설정 */
  border-radius: 8px !important;      /* 입력창 둥근 모서리 */
}
.text-field-custom .v-input__control {
  color: rgb(10, 10, 10) !important;           /* 텍스트 색상도 하얗게 */
}
.custom-white-text {
  color: rgb(11, 11, 11) !important; /* 텍스트 색상을 하얗게 변경 */
}

.login-form {
  margin-top: 10%;
}
</style>