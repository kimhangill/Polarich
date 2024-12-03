import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import swal from "sweetalert";
import { useRecommendStore } from "./recommend";
import { useSavingStore, useDepositStore } from "./productStores";
export const useUserStore = defineStore(
  "user",
  () => {
    const recommendStore = useRecommendStore();
    const recentsearch =ref(['asdasd'])
    const savingStore = useSavingStore()
    const depositStore = useDepositStore()
    const API_URL = "http://127.0.0.1:8000";
    const router = useRouter();
    const token = ref(null);
    const userDesirePeriod = ref(null);
    const userInfo = ref(null);
    const userProfile = ref(null);
    const userNickname = ref(null);
    const UserPortFolio = ref(null)
    const isAuthenticated = ref(false)
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });

    // 회원가입 부분
    const createUser = function (payload) {
      const { username, nickname, password1, password2, age, email, gender, date_of_birth, profileImage } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          nickname,
          email,
          password1,
          password2,
          age,
          date_of_birth,
          profileImage,
          gender,
        },
      })
        .then((res) => {
          const password = password1;
          const payloads = {
            username,
            password,
          };
          login(payloads);
        })
        .catch((err) => {
          swal("Oops", "아이디가 중복되었어요!", "error");
          console.log(err);
        });
    };

    // 로그인
    const login = function (payload) {
      const { username, password } = payload;
      axios({
        method: "post",
        url: `${API_URL}/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          console.log(res.data);
          token.value = res.data.token;
          console.log(token.value);
          
          userInfo.value = res.data.username;
          console.log(depositStore.UserPortFolio);
          getProfile();
          // recommendStore.getRecommendFirst();
          // recommendStore.getRecommendSecond();
          // userDesirePeriod.value = res.data.user.desirePeriod;
          router.push({ name: "MainView" });
          isAuthenticated.value=!isAuthenticated.value
          swal(`${userInfo.value}님 환영합니다!`, {
            buttons: false,
            timer: 1000,
          });
        })
        .catch((err) => {
          swal("Oops", "아이디 혹은 비밀번호가 다릅니다", "error");
          console.log(err);
        });
    };

    // 로그아웃
    const logout = function () {
      axios({
        method: "post",
        url: `${API_URL}/logout/`,
      })
        .then((res) => {
          console.log(res);
          token.value = null;
          userDesirePeriod.value = null;
          userInfo.value = null;
          userProfile.value = null;
          isAuthenticated.value=!isAuthenticated.value
          router.push({ name: "MainView" });
          UserPortFolio.value= null;
          userNickname.value=null
        })
        .catch((err) => {
          console.log(err);
        });
    };
    // UserProfile 부분
    const getProfile = async function () {
      await axios({
        method: "get",
        url: `${API_URL}/api/v1/accounts/profiles/${userInfo.value}/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      }).then((res) => {
        console.log(res.data);
        
        userProfile.value = res.data;
        userNickname.value= res.data.nickname;
        savingStore.favorites = res.data.savings || [];
        depositStore.favorites = res.data.deposits || [];
        UserPortFolio.value = res.data.portfolio || [];

        
      }).catch((err) => console.log(err));
    };

    const setUserPortfolio = function (data) {
      UserPortFolio.value = data
    }
    

    const choicesTranslation = {
      'below_24m': "2,400만 원 이하",
      '24m_to_36m': "2,400만 원 ~ 3,600만 원",
      '36m_to_50m': "3,600만 원 ~ 5,000만 원",
      '50m_to_70m': "5,000만 원 ~ 7,000만 원",
      '70m_to_100m': "7,000만 원 ~ 1억 원",
      'above_100m': "1억 원 이상",
    
      // 직업
      'student': "학생",
      'employee': "직장인",
      'self_employed': "자영업자",
      'retired': "퇴직자",
      'other': "기타",
    
      // 투자 성향
      'conservative': "안정형",
      'moderate': "중립형",
      'aggressive': "공격형",
    
      // 재무 목표
      'home': "주택 마련",
      'retirement': "은퇴 준비",
      'education': "교육 자금",
      'travel': "여행",
      'investment': "투자",
    
      // 투자 경험
      'none': "없음",
      'less_than_1': "1년 미만",
      '1_to_3': "1년 ~ 3년",
      '3_to_5': "3년 ~ 5년",
      'more_than_5': "5년 이상",
    
      // 투자 기간
      'short': "단기",
      'medium': "중기",
      'long': "장기",
    
      // 유동성 선호 여부
      'high': "높음",
      'low': "낮음",
    
      // 위험 수용도
      'low': "낮음",
      'medium': "중간",
      'high': "높음",
    
      // 월 저축액
      'below_300': "30만 원 이하",
      '300_to_500': "30만 원 ~ 50만 원",
      '500_to_1000': "50만 원 ~ 100만 원",
      '1000_to_2000': "100만 원 ~ 200만 원",
      'above_2000': "200만 원 이상",
    
      // 부채 비율
      'below_10': "10% 이하",
      '10_to_30': "10% ~ 30%",
      '30_to_50': "30% ~ 50%",
      '50_to_70': "50% ~ 70%",
      'above_70': "70% 이상",
    
      // 선호하는 투자 유형
      'stocks': "주식",
      'real_estate': "부동산",
      'funds': "펀드",
      'bonds': "채권",
      'cryptocurrency': "암호화폐",
      
      //성별
      'MALE': '남성',
      'FEMALE': '여성',
      'OTHERS': '기타',
    };
    // 오리지날... 일정 급해서 하드코딩 ㅠㅠ
    const reversedChoicesTranslation = {
      "2,400만 원 이하": "below_24m",
      "2,400만 원 ~ 3,600만 원": "24m_to_36m",
      "3,600만 원 ~ 5,000만 원": "36m_to_50m",
      "5,000만 원 ~ 7,000만 원": "50m_to_70m",
      "7,000만 원 ~ 1억 원": "70m_to_100m",
      "1억 원 이상": "above_100m",
      
      // 직업
      "학생": "student",
      "직장인": "employee",
      "자영업자": "self_employed",
      "퇴직자": "retired",
      "기타": "other",
      
      // 투자 성향
      "안정형": "conservative",
      "중립형": "moderate",
      "공격형": "aggressive",
      
      // 재무 목표
      "주택 마련": "home",
      "은퇴 준비": "retirement",
      "교육 자금": "education",
      "여행": "travel",
      "투자": "investment",
      
      // 투자 경험
      "없음": "none",
      "1년 미만": "less_than_1",
      "1년 ~ 3년": "1_to_3",
      "3년 ~ 5년": "3_to_5",
      "5년 이상": "more_than_5",
      
      // 투자 기간
      "단기": "short",
      "중기": "medium",
      "장기": "long",
      
      // 유동성 선호 여부
      "높음": "high",
      "낮음": "low",
      
      // 위험 수용도
      "낮음": "low",
      "중간": "medium",
      "높음": "high",
      
      // 월 저축액
      "30만 원 이하": "below_300",
      "30만 원 ~ 50만 원": "300_to_500",
      "50만 원 ~ 100만 원": "500_to_1000",
      "100만 원 ~ 200만 원": "1000_to_2000",
      "200만 원 이상": "above_2000",
      
      // 부채 비율
      "10% 이하": "below_10",
      "10% ~ 30%": "10_to_30",
      "30% ~ 50%": "30_to_50",
      "50% ~ 70%": "50_to_70",
      "70% 이상": "above_70",
      
      // 선호하는 투자 유형
      "주식": "stocks",
      "부동산": "real_estate",
      "펀드": "funds",
      "채권": "bonds",
      "암호화폐": "cryptocurrency",
    };
    

    return {
      createUser,
      login,
      logout,
      getProfile,
      setUserPortfolio,
      token,
      isLogin,
      API_URL,
      userInfo,
      userProfile,
      userDesirePeriod,
      userNickname,
      UserPortFolio,
      choicesTranslation,
      reversedChoicesTranslation,
      recentsearch,
    };
  },
  { persist: true }
);
