import { defineStore } from 'pinia'
import { EntityDetailsType, CompetitionType, TabSelectedType } from '@/utils/interfaces'

export const useEntityInfoStore = defineStore('entityInfo', {
  state: () => ({ 
    type: 'entity',
    routeName: 'EntityDetails',
    queryType: 'entityPosts',
    details: {} as EntityDetailsType,
    loading: false,
    selectedComptn: null as CompetitionType | null,
    tabSelected: 'allposts' as TabSelectedType,
    refreshing: false,
    singlePost: false,
    singlePostId: ''
  }),
  getters: {
    getSinglePostParams(state) {
      return {entity: state.details.id, id: state.singlePostId }
    }
  },
  actions: {
    patchDetails(data: {entityDetails: EntityDetailsType}) {
      this.$patch({details: data.entityDetails})
    },
    hideSinglePost(value: boolean, id: string='') {
      this.singlePost = !value
      this.singlePostId = id
    }
  },
})