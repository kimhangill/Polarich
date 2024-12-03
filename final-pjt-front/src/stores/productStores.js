import { createProductStore } from "./productStoreHepler";
import { defineStore } from "pinia";
export const useDepositStore = defineStore('deposits', createProductStore('deposits'),{persist:{ paths: ["favorites"],}});
export const useSavingStore = defineStore('savings', createProductStore('savings'),{persist:{ paths: ["favorites"],}});
export const useLoanStore = defineStore('loans', createProductStore('loans'),{persist:{ paths: ["favorites"],}});