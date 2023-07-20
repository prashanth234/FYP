import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({ 
    success: false,
    username: '',
    avatar: '',
    userUpdated: 1,
    auth: false
  }),
  getters: {
  },
  actions: {
    
  },
})