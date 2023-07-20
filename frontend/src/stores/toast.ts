import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({ 
    message: '',
    open: false,
    color: ''
  }),
  getters: {
  },
  actions: {
  },
})