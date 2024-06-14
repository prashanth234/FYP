import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { EntityDetailsType } from '@/utils/interfaces'

export const useEntityInfoStore = defineStore('entityInfo', {
  state: () => ({ 
    details: {} as EntityDetailsType,
    loading: false
  }),
  getters: {
  },
  actions: {
    getEntityDetails(id: string) {
      this.loading = true
  
      const ENTITY_DETAILS = gql`
        query EntityDetails ($id: ID!) {
          entityDetails (id: $id) {
            id,
            name,
            description,
            type,
            image,
            city,
            instagram,
            linkedin,
            facebook,
            userAccess,
            ispublic,
            stats {
              users,
              posts,
              categories {
                name,
                count,
                color
              }
            }
          }
        }
      `
  
      const { onResult, onError } = useQuery(ENTITY_DETAILS, () => ({
        id
      }))
  
      onResult(({data, loading}) => {
        if (!loading) {
          this.$patch({details: data.entityDetails})
          this.loading = false
        }
      })
  
      onError(() => {
        this.loading = false
      })
    }
  },
})