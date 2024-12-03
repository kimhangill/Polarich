<template>
    <v-container class="mt-5">
      <h1 class="section-title">비밀번호 변경</h1>
      <v-form @submit.prevent="submitPasswordChange" ref="form" v-model="isValid">
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              label="현재 비밀번호"
              v-model="currentPassword"
              :rules="[v => !!v || '현재 비밀번호는 필수입니다.']"
              type="password"
              required
            ></v-text-field>
          </v-col>
          <hr>
          <v-col cols="12" sm="6">
            <v-text-field
              label="새로운 비밀번호"
              v-model="newPassword"
              :rules="passwordRules"
              type="password"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              label="비밀번호 확인"
              v-model="confirmPassword"
              :rules="confirmPasswordRules"
              type="password"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-btn color="primary" type="submit" :loading="isLoading" :disabled="isLoading">
          비밀번호 변경
        </v-btn>
        <br>
        <v-btn color="secondary" type="submit" @click="deleteUser">
          회원 탈퇴
        </v-btn>
      </v-form>
      <!-- Snackbar 추가 -->
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useUserStore } from '@/stores/user';
  import axios from 'axios';
  import Swal from 'sweetalert2';
  import { useVuelidate } from '@vuelidate/core';
  import { required, minLength } from '@vuelidate/validators';
  
  // 부모 컴포넌트에 이벤트를 emit하기 위한 설정 (모달 닫기용)
  const emit = defineEmits(['close-page']);
  
  // 사용자 스토어 사용
  const userStore = useUserStore();
  
  // 입력 필드 상태 관리
  const currentPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');
  
  // 유효성 검사 규칙 설정
  const rules = {
    currentPassword: { required },
    newPassword: { required, minLength: minLength(8) },
    confirmPassword: {
      required,
      sameAsNewPassword: (value) => value === newPassword.value || '비밀번호가 일치하지 않습니다.'
    }
  };
  
  // Vuelidate 인스턴스 생성
  const v$ = useVuelidate(rules, { currentPassword, newPassword, confirmPassword });
  
  // 비밀번호 필드에 적용할 추가적인 유효성 검사 규칙
  const passwordRules = [
    v => !!v || '새로운 비밀번호는 필수입니다.',
    v => v.length >= 8 || '비밀번호는 최소 8자 이상이어야 합니다.'
  ];
  
  // 비밀번호 확인 필드에 적용할 유효성 검사 규칙
  const confirmPasswordRules = [
    v => !!v || '비밀번호 확인은 필수입니다.',
    v => v === newPassword.value || '비밀번호가 일치하지 않습니다.'
  ];
  
  // SweetAlert2 커스텀 클래스 정의 (z-index 조정)
  const swalConfig = {
    customClass: {
      popup: 'swal-popup'
    }
  };
  
  // 로딩 상태 관리
  const isLoading = ref(false);
  
  // Snackbar 상태 관리
  const snackbar = ref({
    show: false,
    message: '',
    color: ''
  });
  
  const showSnackbar = (message, color) => {
    snackbar.value.message = message;
    snackbar.value.color = color;
    snackbar.value.show = true;
  };
  
  // 폼 제출 함수
  const submitPasswordChange = async () => {
    // 유효성 검사 수행
    v$.value.$validate();
    if (!v$.value.$invalid) {
      isLoading.value = true;
      try {
        const token = userStore.token; // 사용자 토큰
  
        // 백엔드 요청 데이터 설정
        const requestData = {
          current_password: currentPassword.value,
          new_password1: newPassword.value,
          new_password2: confirmPassword.value
        };
  
        // Axios를 사용하여 백엔드 API로 비밀번호 변경 요청
        await axios.post(
          'http://127.0.0.1:8000/password/change/', // 백엔드 비밀번호 변경 엔드포인트
          requestData,
          {
            headers: {
              Authorization: `Token ${token}`, // 인증이 필요한 경우
              'Content-Type': 'application/json'
            }
          }
        );
  
        // 모달 닫기 이벤트 emit
        emit('close-page');
  
        // 성공 메시지 표시
        Swal.fire({
          title: '변경 완료',
          text: '비밀번호가 성공적으로 변경되었습니다!',
          icon: 'success',
          ...swalConfig
        });
  
        // 필요 시 추가적인 동작 (예: 로그아웃 후 재로그인 등)
        userStore.getProfile(); // 프로필 업데이트 (필요 시)
      } catch (err) {
        console.error(err);
        // 모달 닫기 이벤트 emit
        emit('close-page');
  
        // 오류 메시지 상세화
        let errorMessage = '비밀번호 변경 중 오류가 발생하였습니다. 다시 시도해주세요.';
        if (err.response && err.response.data) {
          // 백엔드에서 반환한 구체적인 오류 메시지 사용
          if (err.response.data.current_password) {
            errorMessage = err.response.data.current_password.join(' ');
          } else if (err.response.data.new_password2) {
            errorMessage = err.response.data.new_password2.join(' ');
          }
        }
  
        // 오류 메시지 표시
        Swal.fire({
          title: '변경 실패',
          text: errorMessage,
          icon: 'error',
          ...swalConfig
        });
      } finally {
        isLoading.value = false;
      }
    }
  };

  const deleteUser = () => {
  // 첫 번째 확인 창
  emit('close-page');
  Swal.fire({
    title: '회원 탈퇴',
    text: '정말로 회원을 탈퇴하시겠습니까?',
    icon: 'warning',
    showCancelButton: true,
    reverseButtons: true,
    customClass: {
      popup: 'swal-popup',
      confirmButton: 'swal-confirm-button',
      cancelButton: 'swal-cancel-button',
    }
  }).then((result) => {
    if (result.isConfirmed) {
      // 두 번째 확인 창
      Swal.fire({
        title: '정말로 탈퇴하시겠습니까?',
        text: '탈퇴 후에는 복구할 수 없습니다.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '탈퇴',
        cancelButtonText: '취소',
        reverseButtons: true,
        customClass: {
          popup: 'swal-popup',
          confirmButton: 'swal-confirm-button',
          cancelButton: 'swal-cancel-button',
        }
      }).then((confirmResult) => {
        if (confirmResult.isConfirmed) {
          // 탈퇴 요청 전송
          axios.delete(`http://127.0.0.1:8000/api/v1/accounts/delete/${userStore.userProfile.username}/`, {
            headers: {
              Authorization: `Token ${userStore.token}`,
              'Content-Type': 'application/json'
            }
          })
          .then(() => {
            // 탈퇴 성공 시
            Swal.fire({
              title: '탈퇴 완료',
              text: '회원 탈퇴가 완료되었습니다. 길잡이별은 당신 위에서, 언제나 빛을 내며 기다리겠습니다!',
              icon: 'success',
              confirmButtonText: '확인',
              customClass: {
                popup: 'swal-popup',
                confirmButton: 'swal-confirm-button',
                cancelButton: 'swal-cancel-button',
              }
            }).then(() => {
              // 로그아웃 및 메인 페이지로 이동
              userStore.logout(); // 사용자 스토어에서 로그아웃 메서드 호출
              router.push({ name: 'MainView' }); // 메인 페이지로 라우팅
            });
          })
          .catch((error) => {
            console.error(error);
            // 탈퇴 실패 시
            Swal.fire({
              title: '탈퇴 실패',
              text: '회원 탈퇴 중 오류가 발생하였습니다. 다시 시도해주세요.',
              icon: 'error',
              confirmButtonText: '확인',
              customClass: {
                popup: 'swal-popup',
                confirmButton: 'swal-confirm-button',
                cancelButton: 'swal-cancel-button',
              }
            });
          });
        }
      });
    }
  });
};

  //회원탈퇴 함수
 
  </script>
  
  <style scoped>
  .section-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 2em;
  }
  
  /* SweetAlert2 팝업의 z-index를 높게 설정 */
  .swal-popup {
    z-index: 10000 !important;
  }

  .swal-confirm-button {
  color: white !important; /* 버튼 글씨 색깔을 하얀색으로 변경 */
  background-color: #003366 !important; /* 버튼 배경색 */
  border: none;
}

.swal-cancel-button {
  color: white !important;
  background-color: #999 !important; /* 버튼 배경색 */
  border: none;
}
  </style>
  