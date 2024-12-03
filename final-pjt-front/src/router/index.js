// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import MapView from "@/views/MapView.vue";
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import ExchangeView from "@/views/ExchangeView.vue";
import ArticleDetailView from "@/views/ArticleDetailView.vue";
import CreateArticleView from "@/views/CreateArticleView.vue";
import SavingProductsView from "@/views/SavingProductsView.vue";
import DepositProductsView from "@/views/DepositProductsView.vue";
import Swal from "sweetalert2";
import { useUserStore } from "@/stores/user";
import LoanProductView from "@/views/LoanProductView.vue";
import PortfolioCreateView from "@/views/PortfolioCreateView.vue";
import PortfolioDetailView from "@/views/PortfolioDetailView.vue";
import PortfolioEditView from "@/views/PortfolioEditView.vue";
import CommunityTypeView from "@/views/CommunityTypeView.vue";
import EditArticleView from "@/views/EditArticleView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import ProfilePosts from "@/views/ProfilePosts.vue";
import ProfileFavorites from "@/views/ProfileFavorites.vue";
import ProfilePortfolio from "@/views/ProfilePortfolio.vue";
import ProductDetailView from "@/views/ProductDetailView.vue";
import ScamLoanComponent from "@/components/ScamLoanComponent.vue";
import HouseScamComponent from "@/components/HouseScamComponent.vue";
import ScamPreventView from "@/views/ScamPreventView.vue";
import LoanList from "@/components/LoanList.vue";


const routes = [
  // 메인 페이지
  {
    path: "/",
    name: "MainView",
    component: MainView,
  },
  // 맵 기능 (미완성)
  {
    path: "/map",
    name: "MapView",
    component: MapView,
  },
  // 유저 관련 기능
  {
    path: "/signup",
    name: "SignupView",
    component: SignupView,
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
  },
  // 프로필, 포트폴리오 관련 기능
  {
    path: '/portfolio/create',
    name: 'PortfolioCreateView',
    component: PortfolioCreateView,
    meta: { requiresAuth: true },
  },

  {
  
    path: '/profile/:username',
    name: 'ProfilePage',
    component: ProfilePage,
    meta: { requiresAuth: true },
    beforeEnter: async (to, from, next) => {
      try {
        const userStore = useUserStore();
        userStore.getProfile(); // 프로필 데이터 가져오기
        next(); // 성공 시 라우트 이동
      } catch (error) {
        console.error(error);
        next('/error'); // 에러가 발생하면 에러 페이지로 이동
      }
    },
    children: [
      {
        path: 'posts',
        name: 'ProfilePosts',
        component: ProfilePosts,
      },
      {
        path: 'favorites',
        name: 'ProfileFavorites',
        component: ProfileFavorites,
      },
      {
        path: '/profile/:username/portfolio',
        name: 'ProfilePortfolio',
        component: ProfilePortfolio, // 포트폴리오 탭 전체를 관리하는 컴포넌트
        meta: { requiresAuth: true },
        children: [
          {
            path: 'edit',
            name: 'PortfolioEditView',
            component: PortfolioEditView,
            meta: { requiresAuth: true },
          },
        ],
      },
      
    ],
  },


  // 게시판 관련 기능
  {
    path: "/community/:type",
    name: "CommunityTypeView",
    component: CommunityTypeView,
    meta: { requiresAuth: false },
    props: true, // type 파라미터를 컴포넌트로 전달
  },

  {
    path: "/community",
    name: "CreateArticleView",
    component: CreateArticleView,
    meta: { requiresAuth: false },
  },
  {
    path: "/article/:id",
    name: "ArticleDetailView",
    component: ArticleDetailView,
    meta: { requiresAuth: false },
  },
  {
    path: "/edit/:id",
    name: "EditArticleView",
    component: EditArticleView,
    meta: { requiresAuth: false },
  },


  {
    path: "/search",
    name: "SearchView",
    component: () => import("@/views/SearchView.vue"),
  },
  {
    path: "/exchange",
    name: "ExchangeView",
    component: ExchangeView,
  },


  // 금융상품, 상품추천 관련 링크
  {
    path: "/savings",
    name: "SavingProductsView",
    component: SavingProductsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/deposits",
    name: "DepositProductsView",
    component: DepositProductsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/loans",
    name: "LoanList",
    component: LoanList,
    meta: { requiresAuth: true },
  },
  {
    path: "/:type/:id",
    name: "ProductDetailView",
    component: ProductDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: "/loan/:id",
    name: "LoanProductView",
    component: LoanProductView,
    meta: { requiresAuth: true },
  },

  {
    path: "/recommendpage",
    name: "RecommendPageView",
    component: () => import("@/views/RecommendPageView.vue"),
  },

  // 금융사기 안전구역
  {
    path: "/scamprevent",
    name: "ScamPreventView",
    component: ScamPreventView,
    children: [
      {
        path: "/scamprevent/house",
        name: "HouseScamComponent",
        component: HouseScamComponent
      },
    
      {
        path: "/scamprevent/loans",
        name: "ScamLoanComponent",
        component: ScamLoanComponent
      },
    ]},



];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if ((to.name === "RecommendPageView" || to.name === "ProfilePortfolio")) {
    if (!userStore.userProfile.portfolio) { 
      Swal.fire({
        icon: "info",
        title: "포트폴리오 작성 필요",
        text: "폴라리치 여정에 함께하기 위한 포트폴리오를 작성해주세요!",
        confirmButtonText: "확인",
      }).then(() => {
        router.push({ name: "PortfolioCreateView" }, {params: { username: userStore.userProfile.username } });
      });
    } 
    
    else if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (userStore.isLogin) {
        next();
      } else {
        Swal.fire({
          title: "로그인이 필요합니다",
          icon: "warning",
        }).then(() => {
          next({ name: "LoginView" });
        });
      }
    } else {
      next();
    }
  }
  else{
    next()
  }
});

export default router;
