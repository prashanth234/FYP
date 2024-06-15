import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionType, categoryType } from '@/utils/interfaces'

// This store stores information about a openend category, through out the app

export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({ 
    details: {} as categoryType,
    loading: true,
    selectedComptn: null as CompetitionType | null,
    tabSelected: 'allposts',
    refreshing: false,
    singlePost: false,
    singlePostId: ''
  }),
  getters: {
  },
  actions: {
    getCategoryInfo(id: string, ionRouter: any = null) {
      this.loading = true

      const CATEGORY_DETAILS = gql`
        query categoryDetails ($id: ID!) {
          categoryDetails (id: $id) {
            id,
            name,
            description,
            oftype,
            competitions {
                id,
                name,
                description,
                lastDate,
                image,
                expired,
                points,
                message
            }
          }
        }
      `
      const { result, onResult, onError } = useQuery(CATEGORY_DETAILS, { id: id })

      onResult(value => {
        if (!value.loading) {
            this.$patch({details: value.data.categoryDetails})
            this.loading = false
        }
      })

      onError((error) => {
        ionRouter?.replace('/')
      })
    },
    hideSinglePost(value: boolean, id: string='') {
      this.singlePost = !value
      this.singlePostId = id
    }
  },
})