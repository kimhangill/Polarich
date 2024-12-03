<template>
  <v-container class="mt-5">
    <h1 class="section-title">유저프로필 편집페이지에요</h1>
    <v-form @submit.prevent="submitProfile" ref="form" v-model="isValid">
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field
            label="닉네임"
            v-model="newNickname"
            :rules="[v => !!v || '닉네임은 필수입니다.']"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field
            label="이메일"
            v-model="newemail"
            :rules="emailRules"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-file-input
            label="프로필 이미지"
            v-model="newprofileImage"
            accept="image/*"
            placeholder="이미지를 선택해주세요"
            :show-size="true"
            truncate-length="15"
            @change="handleImageChange"
          ></v-file-input>
        </v-col>
      </v-row>
      <v-btn color="primary" type="submit">제출</v-btn>
    </v-form>
  </v-container>
</template>

  
  <script setup>
  import { ref } from 'vue';
  import { useUserStore } from '@/stores/user';
  import axios from 'axios';
  import Swal from 'sweetalert2';
  import { useVuelidate } from '@vuelidate/core';
  import { required, email } from '@vuelidate/validators';
  import { defineEmits } from 'vue';
  const props = defineProps({
    profile: Object
  });

  const emit = defineEmits(['close-page'])
  
  const userStore = useUserStore();
  
  // 초기 값 설정
  const newNickname = ref(props.profile.nickname);
  const newemail = ref(props.profile.email);
  const newprofileImage = ref(props.profile.profileImage);
  
  // 유효성 검사 규칙
  const rules = {
    newNickname: { required },
    newemail: { required, email }
  };
  
  const v$ = useVuelidate(rules, { newNickname, newemail });
  
  // 이메일 유효성 검사 규칙
  const emailRules = [
    v => !!v || '이메일은 필수입니다.',
    v => /.+@.+\..+/.test(v) || '유효한 이메일을 입력해주세요.'
  ];
  
  // SweetAlert2 커스텀 클래스 정의 (z-index 조정)
  const swalConfig = {
    customClass: {
      popup: 'swal-popup'
    }
  };
  
  const submitProfile = async () => {
    v$.value.$validate();
    if (!v$.value.$invalid) {
      try {
        const token = userStore.token; // 토큰이 userStore에 있다고 가정
        const username = userStore.userProfile.username; // userInfo가 userStore에 있다고 가정
        console.log(token);
        
        const formData = new FormData();
        formData.append('nickname', newNickname.value);
        formData.append('email', newemail.value);
        if (newprofileImage.value && newprofileImage.value !== props.profile.profileImage) {
          formData.append('profileImage', newprofileImage.value);
        }
  
        await axios.put(
          `${userStore.API_URL}/api/v1/accounts/profiles/${username}/`,
          formData,
          {
            headers: {
              Authorization: `Token ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        emit('close-page')
        Swal.fire({
          title: '수정 완료',
          text: '프로필 수정이 완료되었습니다!',
          icon: 'success',
          ...swalConfig
        });
        userStore.getProfile();
      } catch (err) {
        console.error(err);
        emit('close-page')
        Swal.fire({
          title: '수정 실패',
          text: '수정 과정에서 오류가 발생하였습니다!',
          icon: 'error',
          ...swalConfig
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .section-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 2em;
  }
  
  /* SweetAlert2 팝업의 z-index를 높게 설정 */
  .swal-popup {
    z-index: 9999
  }
  </style>
  