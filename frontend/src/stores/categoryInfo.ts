import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionInfo } from '@/utils/interfaces'

// This store stores information about a openend category, through out the app

export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({ 
    id: '',
    name: '',
    description: '',
    oftype: '',
    competitionSet: [] as CompetitionInfo[],
    loading: true,
    selectedComptn: null as CompetitionInfo | null
  }),
  getters: {
  },
  actions: {
    getCategoryInfo (id: string, ionRouter: any) {
      this.loading = true

      const CATEGORY_DETAILS = gql`
      query categoryDetails ($id: ID!) {
          categoryDetails (id: $id) {
              id,
              name,
              description,
              oftype,
              competitionSet {
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
            this.$patch(value.data.categoryDetails)
            this.loading = false
        }
      })

      onError((error) => {
        ionRouter.replace('/')
      })
    }
  },
})