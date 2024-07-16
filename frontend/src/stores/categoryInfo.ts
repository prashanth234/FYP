import { defineStore } from 'pinia'
import { CompetitionType, CategoryType, TabSelectedType } from '@/utils/interfaces'

// This store stores information about a openend category, through out the app

export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({
    type: 'category',
    routeName: 'CategoryDetails',
    queryType: 'allPosts',
    details: {} as CategoryType,
    loading: true,
    selectedComptn: null as CompetitionType | null,
    tabSelected: 'allposts' as TabSelectedType,
    refreshing: false,
    singlePost: false,
    singlePostId: ''
  }),
  getters: {
    getSinglePostParams(state) {
      return {category: state.details.id, id: state.singlePostId }
    }
  },
  actions: {
    patchDetails(data: {categoryDetails: CategoryType}) {
      this.details = data.categoryDetails
    },
    hideSinglePost(value: boolean, id: string='') {
      this.singlePost = !value
      this.singlePostId = id
    }
  },
})