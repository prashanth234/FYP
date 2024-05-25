import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { EntityType } from '@/utils/interfaces'

export const useEntityStore = defineStore('entity', {
  state: () => ({ 
    entities: [] as EntityType[],
    loading: false
  }),
  getters: {
  },
  actions: {
    getEntities () {
      if (this.entities.length) { return }

      this.loading = true
      
      const { result: data, loading, onResult, onError } = useQuery(gql`
                                        query Entities {
                                          entities {
                                            id,
                                            name,
                                            description,
                                            image,
                                            city, 
                                            type,
                                            ispublic,
                                            userAccess,
                                            stats {
                                              users,
                                              posts
                                            }
                                          }
                                        }
                                      `)


      onResult(({data, loading}) => {
        if (!loading) {
          this.entities = data.entities
          this.loading = false
        }
      })

      onError(() => {
        this.loading = false
      })
    }
  },
})