<template>
    <v-container class="profile-container">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <v-card class="profile-card">
            <v-card-text>
              <div class="profile-header">
                <!-- 프로필 이미지 -->
                <v-avatar size="100" class="profile-avatar">
                  <img
                    width="100%"
                    height="100%"
                    :src="'http://127.0.0.1:8000' + profile.profileImage"
                    alt="프로필 이미지"
                  />
                </v-avatar>
                <!-- 닉네임과 사용자명 -->
                <div class="profile-info">
                  <h4 class="profile-nickname section-title">{{ profile.nickname }}</h4>
                  <p class="profile-username">@{{ profile.username }}</p>
                </div>
              </div>
              <!-- 추가 정보 -->
              <div class="profile-details">
                <p><strong>이메일:</strong> {{ profile.email }}</p>
                <p><strong>생년월일:</strong> {{ profile.date_of_birth }}</p>
                <p><strong>성별:</strong> {{ profile.gender }}</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  defineProps({ profile: Object });
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 100%; /* 컨테이너 전체 너비 사용 */
    padding: 0 16px;
  }
  
  .profile-card {
    padding: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
    width: auto; /* 카드 너비 제한 해제 */
  }
  
  .profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap; /* 줄바꿈 허용 */
  }
  
  .profile-avatar {
    margin-right: 20px;
  }
  
  .profile-info {
    flex-grow: 1; /* 남은 공간 모두 사용 */
    min-width: 0; /* overflow 문제 방지 */
  }
  
  .profile-nickname {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
    white-space: nowrap; /* 줄바꿈 방지 */
    overflow: hidden; /* 넘치는 텍스트 숨기기 */
    text-overflow: ellipsis; /* 넘치는 텍스트에 ... 표시 */
  }
  
  .profile-username {
    font-size: 1rem;
    color: rgb(143, 139, 139);
    margin: 5px 0 0 0;
  }
  
  .profile-details {
    margin-top: 20px;
    line-height: 1.8;
  }
  
  .profile-details p {
    margin: 0;
  }
  
  .profile-details strong {
    color: #003366;
  }
  </style>
  