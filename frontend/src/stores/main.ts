import { defineStore } from 'pinia'

// Use this store to store common and global data

export const useMainStore = defineStore('main', {
  state: () => ({ 
    pageloading: false
  }),
  getters: {
  },
  actions: {
  },
})