import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import swal from "sweetalert";

export const useCommentStore = defineStore(
  "comment",
  () => {
    // 유저 토큰 확보용
    const userStore = useUserStore();
    const token = userStore.token
    const comments = ref([])
    const userComments = ref([])
    //메인 url
    const API_URL = "http://127.0.0.1:8000/api/v1/";

    // 댓글은 객체 전체가 아티클 디테일에 딸려오니 지정할 필요 없음

    const router = useRouter();

    // articleId, content를 payload에 넣어줌.
    // 댓글은 C,U,D 과정에서 팝업 필요 없음.
    const getCommentByUser =  (username) => {
       axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${username}/comments/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then((res) => {
        userComments.value = res.data;
      })
      .catch((err) => {
        console.error('사용자 댓글을 가져오는 중 오류 발생:', err);
      });
    };

    const getComment =  function (articleId) {
      axios({
        methd:'get',
        url:`${API_URL}articles/${articleId}/comments/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      }).then((res)=> {comments.value = res.data
        return res.data
      }).catch((err)=>{console.log(err);
      })
    }

    const postComment = async (payload) => {
      console.log(payload);
      try {
        await axios.post(`${API_URL}comments/`, payload, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        swal("성공", "댓글이 작성되었습니다.", "success");
      } catch (error) {
        swal("에러", "댓글 작성 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };


    const putComment = async (commentId, payload) => {
      try {
        console.log(commentId);
        console.log(payload);

        await axios.put(`${API_URL}comments/${commentId}/`, payload, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
      } catch (error) {
        console.error(error);
      }
    };

    const deleteComment = async (commentId) => {
      try {
        await axios.delete(`${API_URL}comments/${commentId}/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
      } catch (error) {
        swal("에러", "댓글 삭제 중 문제가 발생했습니다.", "error");
        console.error(error);
      }
    };

    return { postComment, deleteComment, putComment, getComment, getCommentByUser,comments, userComments};
  }
);
