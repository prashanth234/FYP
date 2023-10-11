import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionInfo, Reward } from '@/mixims/interfaces'

export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({ 
    id: '',
    name: '',
    description: '',
    oftype: '',
    competitionSet: [] as CompetitionInfo[],
    loading: true,
    selectedComptn: null as CompetitionInfo | null,
    selectedComptnRewards: [] as Reward[]
  }),
  getters: {
  },
  actions: {
    getCategoryInfo (id: string) {
      this.loading = true
      const { result, onResult } = useQuery(gql`
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
                                                expired
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
    },
    getComptnRewards (id: string) {
      const { result, onResult } = useQuery(gql`
                                    query competitionDetails ($id: Int!) {
                                      competitionDetails (id: $id) {
                                            id,
                                            rewards {
                                              position,
                                              points
                                            }
                                        }
                                    }
                                    `, {
                                    id: id,
                                  })
                                  
      onResult(({data, loading}) => {
        if (!loading && this.selectedComptn) {
          this.selectedComptnRewards = data.competitionDetails.rewards
        }
      })
    }
  },
})