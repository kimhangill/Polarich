import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "./user";

export const useRecommendStore = defineStore('recommend', () => {
    const API_URL = "http://127.0.0.1:8000/products";
    const recommendFirst = ref([])
    const recommendSecond = ref([])
    const userStore = useUserStore()
    // console.log(userStore.userInfo)
    const getRecommendFirst = function () {
        axios({
        method: 'get',
        url: `${API_URL}/recommend/deposit/${userStore.userInfo.username}/`,
        headers: {
            Authorization: `Token ${userStore.token}`,
        }
        })
        .then((response) => {
            recommendFirst.value = []
            response.data.forEach((item) => {
                recommendFirst.value.push(item)
            })
            axios({
                method: 'get',
                url: `${API_URL}/recommend/saving/${userStore.userInfo.username}/`,
                headers: {
                    Authorization: `Token ${userStore.token}`,
                }
                })
                .then((response) => {
                    response.data.forEach((item) => {
                        recommendFirst.value.push(item)
                    })
                })
                .catch((error) => {
                    console.log(error)
                })
        })
        .catch((error) => {
            console.log(error)
        })
    }

    const getRecommendSecond = function () {
        axios({
        method: 'get',
        url: `${API_URL}/recommend/deposit/second/${userStore.userInfo.username}/`,
        headers: {
            Authorization: `Token ${userStore.token}`,
        }
        })
        .then((response) => {
            recommendSecond.value = []
            response.data.forEach((item) => {
                recommendSecond.value.push(item)
            })
            axios({
                method: 'get',
                url: `${API_URL}/recommend/saving/second/${userStore.userInfo.username}/`,
                headers: {
                    Authorization: `Token ${userStore.token}`,
                }
                })
                .then((response) => {
                    response.data.forEach((item) => {
                        recommendSecond.value.push(item)
                    })
                })
                .catch((error) => {
                    console.log(error)
                })
        })
        .catch((error) => {
            console.log(error)
        })
    }
    return { getRecommendFirst, recommendFirst, getRecommendSecond, recommendSecond }
}, { persist: true }
);