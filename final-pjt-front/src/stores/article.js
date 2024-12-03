import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import swal from "sweetalert";

export const useArticleStore = defineStore(
  "article",
  () => {
    // 유저 토큰 확보용
    const userStore = useUserStore();
    const token = userStore.token

    //메인 url
    const API_URL = "http://127.0.0.1:8000/api/v1/";

    // 아티클 저장할 곳 
    const articlesList = ref([]);
    const articleDetail = ref(null);
    const router = useRouter();
    const userArticles = ref([])
    const searchresults = ref([])
    // 게시글 리스트 GET

    const getArticleByUser =  (username) => {
       axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${username}/articles/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        userArticles.value = res.data;
      })
      .catch((err) => {
        console.error('사용자 게시글을 가져오는 중 오류 발생:', err);
      });
    };

    const getArticleList = async (type = "general") => {
      try {
        const response = await axios.get(`${API_URL}articles/?type=${type}`);
        articlesList.value = response.data.results;
        console.log(articlesList.value);
        
      } catch (error) {
        swal("에러", "게시글 목록을 불러오는 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };

    const searchgetArticleList = async (searchQuery) => {
      try {
        const response = await axios.get(`${API_URL}articles/`, {
          params: {
            search: searchQuery,
          },
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        }).then((res) => 
          {searchresults.value = res.data.results;
          console.log(searchresults.value);}
        )

        
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };

    const getArticleDetail = async (articleId) => {
      try {
        const response = await axios.get(`${API_URL}articles/${articleId}/`);
        articleDetail.value = response.data;
        console.log(articleDetail.value);
      } catch (error) {
        swal("에러", "게시글 정보를 불러오는 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };


    const postArticle = async (payload) => {
      try {
        await axios.post(`${API_URL}articles/`, payload, {
          headers: {
            Authorization: `Token ${token}`,
          },
        }).then((res)=>{
          console.log(res.data);
          swal("성공", "게시글이 작성되었습니다.", "success");
          router.push(`/article/${res.data.id}`);
        })
        
        
      } catch (error) {
        swal("에러", "게시글 작성 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };

    const putArticle = async (articleId, payload) => {
      try {
        await axios.put(`${API_URL}articles/${articleId}/`, payload, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        swal("성공", "게시글이 수정되었습니다.", "success");
        router.push(`/article/${articleId}`);
      } catch (error) {
        swal("에러", "게시글 수정 중 문제가 발생했습니다.", "error");
        console.error("Error while updating article:", error);
      }
    };
    

    const deleteArticle = async (articleId,type) => {
      try {
        await axios.delete(`${API_URL}articles/${articleId}/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        swal("성공", "게시글이 삭제되었습니다.", "success");
        router.push(`/community/${type}`);
      } catch (error) {
        swal("에러", "게시글 삭제 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };

    return { articlesList, articleDetail, userArticles, searchresults, getArticleByUser, getArticleList, getArticleDetail, postArticle, deleteArticle, putArticle, searchgetArticleList };
  },
  { persist: true }
);
