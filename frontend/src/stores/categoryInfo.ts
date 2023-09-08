import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionInfo } from '@/mixims/interfaces'

export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({ 
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
    getCategoryInfo (id: string) {
      this.loading = true
      const { result, onResult } = useQuery(gql`
                                    query ($id: Int!) {
                                        categoryDetails (id: $id) {
                                            name,
                                            description,
                                            oftype,
                                            competitionSet {
                                                id,
                                                name,
                                                description,
                                                lastDate,
                                                points,
                                                image
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
    }
  },
})