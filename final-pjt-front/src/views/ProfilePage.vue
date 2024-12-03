<template>
  <v-container class="profile-container" width="1500px">
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card class="profile-card">
          <v-card-text class="profile-main">
            <!-- 프로필 이미지 -->
            <v-avatar size="100" class="profile-avatar">
              <img :src="'http://127.0.0.1:8000' + user.profileImage" width="100%" height="100%" alt="프로필 이미지" />
            </v-avatar>
            <!-- 닉네임 -->
            <p class="profile-nickname">{{ user.nickname }}</p>
            <!-- 사용자명 -->
            <p class="profile-username">@{{ user.username }}</p>
          </v-card-text>

          <!-- 프로필 상세보기 및 편집 버튼 -->
          <v-card-actions class="profile-actions">
            <v-btn
              color="secondary"
              outlined
              class="profile-button"
              @click="showProfile = true"
            >
              상세 프로필
            </v-btn>
            <v-btn
              color="secondary"
              outlined
              class="profile-button"
              @click="showEditProfile = true"
            >
              프로필 편집
            </v-btn>
            <v-btn
              color="deep-orange"
              outlined
              class="profile-button"
              @click="showEditPasswordProfile = true"
            >
              비밀번호 변경
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 탭 내비게이션 -->
    <ProfileTabs />

    <!-- PortfolioFormComponent 모달 -->
    <v-dialog v-model="showProfile" max-width="600px"  height="300px">
      <v-card>
        <UserProfileDetailComponet :profile="user" @close="showProfile = false" />
      </v-card>
    </v-dialog>
    <!-- 프로필 편집 모달 -->
    <v-dialog v-model="showEditProfile" max-width="540px" height="1000px">
      <v-card>
        <UserProfileEditComponet :profile="user" @close="showEditProfile = false" @close-page="showEditProfile = false"/>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showEditPasswordProfile" max-width="540px" height="1000px">
      <v-card>
        <UserPasswordEditComponet :profile="user" @close="showEditPasswordProfile = false" @close-page="showEditPasswordProfile = false"/>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import ProfileTabs from '@/components/ProfileTabs.vue';
import UserProfileDetailComponet from '@/components/UserProfileDetailComponet.vue';
import UserPasswordEditComponet from '@/components/UserPasswordEditComponet.vue';
import UserProfileEditComponet from '@/components/UserProfileEditComponet.vue';
const userStore = useUserStore();
const user = computed(()=>userStore.userProfile)
const showProfile = ref(false);
const showEditProfile = ref(false)
const showEditPasswordProfile = ref(false)
onMounted(() => userStore.getProfile());
</script>

<style scoped>
.profile-container {
  max-width: 900px;
  margin: 0 auto;
}

.profile-card {
  text-align: center;
  margin-top: 30px;
  margin-bottom: 30px;
  padding: 20px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
}

.profile-main {
  margin-bottom: 20px;
}

.profile-avatar {
  margin-bottom: 10px;
}

.profile-nickname {
  font-weight: bold;
  font-size: 1.8em;
  margin-bottom: 5px;
}

.profile-username {
  color: #888;
  font-size: 1.1em;
  margin-bottom: 20px;
}

.profile-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.profile-button {
    text-decoration: none;
    padding: 10px 15px;
    border-radius: 25px;
    background-color: #f7f7f7;
    color: #333;
    font-weight: bold;
    transition: background-color 0.2s, box-shadow 0.2s;
  }
</style>
