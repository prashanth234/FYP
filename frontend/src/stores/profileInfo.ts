import { defineStore } from 'pinia'
import { TabSelectedType } from '@/utils/interfaces'

// This store stores information about a profile

export const useProfileInfoStore = defineStore('profileInfo', {
  state: () => ({
    type: 'profile',
    routeName: 'profile',
    queryType: 'myPosts',
    details: {id: ''},
    loading: false,
    selectedComptn: null,
    tabSelected: 'allposts' as TabSelectedType,
    refreshing: false,
    singlePost: false,
    singlePostId: '',
    // When route is changed from details page store details are cleared, so if set to true clear store manually after usage
    preserve: false
  }),
  getters: {
    getSinglePostParams(state) {
      return {id: ''}
    }
  },
  actions: {
    patchDetails() {
    },
    hideSinglePost() {
    }
  },
})