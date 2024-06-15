import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { EntityDetailsType, CompetitionType } from '@/utils/interfaces'

export const useEntityInfoStore = defineStore('entityInfo', {
  state: () => ({ 
    details: {} as EntityDetailsType,
    loading: false,
    selectedComptn: null as CompetitionType | null
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
            competitions {
              id,
              name,
              description,
              lastDate,
              image,
              expired,
              points,
              message
            },
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