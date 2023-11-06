import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionInfo } from '@/mixims/interfaces'

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
      const { result, onResult, onError } = useQuery(gql`
                                    query categoryDetails ($id: Int!) {
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
                                                points
                                            }
                                        }
                                    }
                                    `, {
                                    id: id,
                                  })

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