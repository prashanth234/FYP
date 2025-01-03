import { defineStore } from 'pinia'

// Use this store to store common and global data

export const useMainStore = defineStore('main', {
  state: () => ({ 
    pageloading: false,
    entity: ''
  }),
  getters: {
  },
  actions: {
    getentity() {
      if (!this.entity) {
        const hostname = window.location.hostname
        const parts = hostname.split('.')
        // TODO: length should be greater than 2
        this.entity = parts.length > 1 ? parts[0] : ''
      }
    }
  },
})