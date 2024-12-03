import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "./user";
import Swal from "sweetalert2";

const BASE_URL = "http://127.0.0.1:8000/api/v1/products/";

export function createProductStore(endpoint) {
  return function () {
    const products = ref([]);
    const loading = ref(false);
    const favorites = ref([]);
    const searchQuery = ref("");
    const sortKey = ref("-id");
    const page = ref(1);
    const hasMore = ref(true);
    const userStore = useUserStore();
    const userSavings = ref([])
    const userDeposits = ref([])
    const recommenddeposits = ref([])
    const recommendsavings = ref([])
    const searchresults = ref([])
    const avgDeposit = ref(null)
    const avgSaving = ref(null)
    const myDeposit = ref(null)
    const mySaving = ref(null)
    const fetchProducts = async (isAppending = false) => {
      if (loading.value || !hasMore.value) return;

      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}${endpoint}/`, {
          params: {
            search: searchQuery.value,
            sort: sortKey.value,
            page: page.value,
          },
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });

        const fetchedProducts = response.data.results;

        if (isAppending) {
          products.value = [...products.value, ...fetchedProducts];
        } else {
          products.value = fetchedProducts;
        }

        if (fetchedProducts.length < 25) {
          hasMore.value = false;
        } else {
          page.value += 1;
        }
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        loading.value = false;
      }
    };

    const fetchProductDetail = async (id) => {
      try {
        const res = await axios.get(`${BASE_URL}${endpoint}/${id}/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        console.log(res.data);
        return res.data;
      } catch (err) {
        console.log(err);
      }
    };

    const searchProducts = async (searchQuery) => {
      try {
        const response = await axios.get(`${BASE_URL}${endpoint}/`, {
          params: {
            search: searchQuery,
            sort: sortKey.value,
            page: 1,
          },
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        if (!response.data.results.length) {
        }
        searchresults.value = response.data.results;
        return response.data.results
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };

    const updateSearchQuery = (query) => {
      searchQuery.value = query;
      page.value = 1;
      hasMore.value = true;
      fetchProducts();
    };

    const updateSortKey = (key) => {
      sortKey.value = key;
      page.value = 1;
      hasMore.value = true;
      fetchProducts();
    };

    const addFavorite = async (productId) => {
      try {
        const response = await axios.post(
          `${BASE_URL}add_favorite/`,
          {
            product_type: `${endpoint}`,
            product_id: productId,
          },
          {
            headers: {
              Authorization: `Token ${userStore.token}`,
            },
          }
        );

        if (response.data.message.includes("추가")) {
          favorites.value.push(productId);
        } else {
          favorites.value = favorites.value.filter((id) => id !== productId);
        }
      } catch (error) {
        console.error("Failed to update favorite:", error);
      }
    };
    const getRecommendations = () => {
      axios({
        method: 'get',
        url: `${BASE_URL}recommendations/`,
        headers: {
          Authorization: `Token ${userStore.token}`,
        },
      })
        .then((res) => {
          // 각 추천 타입별 데이터 보관
          recommenddeposits.value = {
            popular: res.data.popular.recommended_deposits,
            occupation: res.data.occupation.recommended_deposits,
            financial_goal: res.data.financial_goal.recommended_deposits,
            age_gender: res.data.age_gender.recommended_deposits,
          };
  
          recommendsavings.value = {
            popular: res.data.popular.recommended_savings,
            occupation: res.data.occupation.recommended_savings,
            financial_goal: res.data.financial_goal.recommended_savings,
            age_gender: res.data.age_gender.recommended_savings,
          };
        })
        .catch((err) => console.error('추천 데이터 로드 중 오류 발생:', err));
    };
  


    const getFavorites = () => {

      
      axios({
        method: 'get',
        url: `${BASE_URL}favorites/`,
        headers: {  // 헤더는 요청 객체 내부에 포함되어야 함
          Authorization: `Token ${userStore.token}`,
        },
      })
        .then((res) => {
          const { savings, deposits } = res.data;
          // ref 값 업데이트
          userSavings.value = savings || [];
          userDeposits.value = deposits || [];
          
        })
        .catch((err) => console.log(err));
    }

    return {
      products,
      loading,
      favorites,
      searchQuery,
      sortKey,
      page,
      hasMore,
      userDeposits,
      userSavings,
      avgDeposit,
      avgSaving,
      myDeposit,
      mySaving,
      fetchProducts,
      updateSearchQuery,
      updateSortKey,
      addFavorite,
      fetchProductDetail,
      getFavorites,
      getRecommendations,
      recommenddeposits,
      recommendsavings,
      searchresults,
      searchProducts,
    };
  };
}
