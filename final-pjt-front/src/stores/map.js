import { defineStore } from "pinia";
import { ref } from "vue";
import { KakaoMap } from "vue3-kakao-maps";

export const useMapStore = defineStore("map", () => {
  const API_KEY = '351e57c2ad3ddbb6893836e5f96207d7'


  return { API_KEY, };
});
