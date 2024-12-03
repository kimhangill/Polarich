<template>
  <v-container class="sign-form">
    <v-sheet 
      class="mx-auto px-12 login-sheet"
      width="40%"
      elevation="4"
      height="auto"
      max-height="86vh"
      rounded
      style="border-radius: 10px; min-height: 880px;"
    >
      <!-- REGISTER 제목 -->
      <v-row class="text-center">
        <v-col >
          <h1 style="font-weight: bold; font-size: 28px;" class="section-title">REGISTER</h1>
        </v-col>
      </v-row>
  
      <!-- 폼 -->
      <v-container class="px-0 pb-0">
        <v-form class="my-0 px-4" ref="form" @submit.prevent="submitForm">
          <v-row dense>
            <!-- Username -->
            <v-col cols="12" style="margin-top: -10px;">
              <v-text-field
                class="line-field text-field-white-error v-input__hint"
                hint="사용할 아이디를 입력 해주세요"
                label="아이디"
                variant="underlined"
                v-model="state.username"
                @blur="v$.username.$touch"
                :error-messages="v$.username.$error ? ['아이디는 최대 20자리 입니다.'] : []"
              ></v-text-field>
            </v-col>
  
            <!-- Nickname -->
            <v-col cols="12" style="margin-bottom: -10px;">
              <v-text-field
                class="line-field v-input__hint"
                label="닉네임*"
                variant="underlined"
                hint="사용할 닉네임을 입력해주세요"
                v-model="state.nickname"
                @blur="v$.nickname.$touch"
                :error-messages="v$.nickname.$error ? ['닉네임은 최대 20자리 입니다.'] : []"
              ></v-text-field>
            </v-col>
  
            <!-- Password -->
            <v-col cols="12" style="margin-bottom: -10px;">
              <v-text-field
                class="line-field v-input__hint"
                hint="특수문자를 제외한 10자리 이상을 입력해주세요"
                label="비밀번호*"
                variant="underlined"
                type="password"
                v-model="state.password1"
                @blur="v$.password1.$touch"
                :error-messages="v$.password1.$error ? ['비밀번호는 최소 8자리 이상입니다.'] : []"
              ></v-text-field>
            </v-col>
  
            <!-- Confirm Password -->
            <v-col cols="12" style="margin-bottom: -10px;">
              <v-text-field
                class="line-field v-input__hint"
                hint="동일한 비밀번호를 입력해주세요"
                label="비밀번호 확인*"
                variant="underlined"
                type="password"
                v-model="state.password2"
                @blur="v$.password2.$touch"
                :error-messages="v$.password2.$error ? ['비밀번호가 일치하지 않습니다.'] : []"
              ></v-text-field>
            </v-col>
  
            <!-- Email -->
            <v-col cols="12" style="margin-bottom: -10px;">
              <v-text-field
                class="line-field v-input__hint"
                hint="사용할 이메일을 입력해주세요"
                label="이메일*"
                variant="underlined"
                type="email"
                v-model="state.email"
                @blur="v$.email.$touch"
                :error-messages="v$.email.$error ? ['올바른 이메일 주소를 입력해주세요.'] : []"
              ></v-text-field>
            </v-col>
  
            <!-- 생년월일 -->
            <v-col cols="12" style="margin-bottom: -10px;">
              <v-dialog
                v-model="state.dialog"
                activator="parent"
                :close-on-content-click="false"
                transition="dialog-transition"
                max-width="290px"
              >
                <template #activator="{ props }">
                  <v-text-field
                    class="line-field v-input__hint"
                    prepend-inner-icon="mdi-calendar"
                    hint="생년월일을 선택해주세요"
                    label="생년월일*"
                    variant="underlined"
                    v-model="state.birthday"
                    readonly
                    v-bind="props"
                    :error-messages="v$.birthday.$error ? ['유효한 생년월일을 선택해주세요.'] : []"
                  ></v-text-field>
                </template>
                <v-card>
                  <v-card-title class="headline grey lighten-2">생년월일 선택</v-card-title>
                  <v-date-picker
                    v-model="state.birthday"
                    @change="state.dialog = false"
                    :max="new Date().toISOString().split('T')[0]"
                    :min="new Date(new Date().setFullYear(new Date().getFullYear() - 99)).toISOString().split('T')[0]"
                  ></v-date-picker>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="state.dialog = false">취소</v-btn>
                    <v-btn text @click="state.dialog = false">확인</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-col>
  
            <!-- gender -->
            <v-col cols="12">
              <v-select
                class="line-field v-input__hint"
                prepend-inner-icon="mdi-account"
                hint="성별을 선택해주세요"
                label="Gender*"
                variant="underlined"
                :items="['Male', 'Female', 'Other']"
                v-model="state.gender"
                @blur="v$.gender.$touch"
                :error-messages="v$.gender.$error ? ['성별을 선택해주세요.'] : []"
              ></v-select>
            </v-col>
  
            <!-- Profile Image -->
            <v-col cols="12" style="margin-top: -20px">
              <v-file-input
                class="line-field v-input__hint"
                label="프로필 이미지"
                prepend-inner-icon="mdi-camera"
                variant="underlined"
                accept="image/*"
                v-model="state.profileImage"
                hint="프로필 이미지를 업로드해주세요"
                :error-messages="v$.profileImage.$error ? ['이미지 파일을 선택해주세요.'] : []"
              ></v-file-input>
            </v-col>
  
            <!-- Terms & Conditions + Submit -->
            <v-col cols="12" >
              <v-row class="d-flex flex-column align-center mt-1" >
                <!-- Terms -->
                <v-checkbox
                  class="mt-0 mb-1"
                
                  color="#F9A825"
                  label="(필수) 서비스 이용약관 동의"
                  value="service"
                  v-model="selected"
                ></v-checkbox>
                <v-checkbox
                  class="mt-0 mb-1"
                  color="#F9A825"
                  label="(필수) 개인정보 처리 동의"
                  value="info"
                  v-model="selected"
                ></v-checkbox>
  
                <!-- Submit Button -->
                <v-btn
                  class="button-custom"
                  type="submit"
                  style="width: 100%; height: 50px; margin-top: 5px;"
                >
                  다음
                </v-btn>
              </v-row>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-sheet>

  </v-container>
</template>


<script setup>
import { reactive, computed, ref } from "vue";
import useVuelidate from "@vuelidate/core";
import { required, minLength, maxLength, sameAs, email } from "@vuelidate/validators";
import { useUserStore } from "@/stores/user";

const selected = ref([]);
const userStore = useUserStore();

const state = reactive({
  username: null,
  nickname: null,
  password1: "",
  password2: "",
  email: null,
  profileImage: null,
  birthday: null,
  gender: null,
  dialog: false,
});

const password1 = computed(() => state.password1);

const rules = computed(() => ({
  username: { required, maxLength: maxLength(20) },
  nickname: { required, maxLength: maxLength(20) },
  password1: { required, minLength: minLength(8), maxLength: maxLength(128) },
  password2: { required, sameAsPassword1: sameAs(password1) },
  email: { required, email },
  profileImage: {},
  birthday: { required },
  gender: { required },
}));

const v$ = useVuelidate(rules, state);

const submitForm = () => {
  v$.value.$validate();
  if (selected.value.length !== 2) {
    alert("모든 약관에 동의 해주셔야 합니다.");
    return;
  }
  if (!v$.value.$error) {
    const date = new Date(state.birthday);
    const formattedDate = date.toISOString().split("T")[0];
    const payload = {
      username: state.username,
      nickname: state.nickname,
      password1: state.password1,
      password2: state.password2,
      email: state.email,
      profileImage: state.profileImage,
      date_of_birth: formattedDate,
      gender: state.gender,
    };
    userStore.createUser(payload);
    alert("회원가입 성공!");
  } else {
    alert("입력 내용을 확인해주세요.");
  }
};
</script>

<style scoped>
/* 로그인 창 스타일 */
.login-sheet {
  background-color: rgba(255, 255, 255, 0.6); /* 반투명 흰색 배경 */
  backdrop-filter: blur(10px); /* 블러 효과 */
  max-height: 120vh; /* 세로 최대 길이 추가 */
  min-height: 600px; /* 최소 높이 추가 */
}

/* 텍스트 필드 스타일 */
.line-field {
  margin-bottom: 1px; /* 필드 간격 축소 */
  border-radius: 0;
  box-shadow: none;
  
}

.line-field .v-input__control {
  border-bottom: none !important;
  color: black; /* 텍스트를 검정색으로 */
}

/* 체크박스 간격 축소 */
.v-checkbox {
  margin-top: 2px; /* 체크박스 위아래 간격 축소 */
}
h2 {
  color: black; /* REGISTER 제목 검정색 */
}

/* 버튼 스타일 */
.button-custom {
  color: white;
  background-color: blue;
  border-radius: 24px;
  margin-top: 10px; /* 버튼 간격 축소 */
}

.sign-form {
  margin-top: 2%;
}
</style>
