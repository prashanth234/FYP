import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { EntityDetailsType, CompetitionType, TabSelectedType } from '@/utils/interfaces'
import { RouteLocationNormalizedLoaded } from 'vue-router'

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
    getDetails(id: string, route: RouteLocationNormalizedLoaded) {
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
              id,
              users,
              posts,
              categories {
                id,
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
          // When a post is created or when user is logged/logout, entity details are changed as a result onResult method is called and store is updated.
          // So making sure that store gets updated, only when current page is entity details page.
          // Store should only hold the current page details. If the store holds entity details while patching, patch will fail as __typename is only readonly
          if (route.params.id == id) {
            this.$patch({details: data.entityDetails})
          }
          this.loading = false
        }
      })
  
      onError(() => {
        this.loading = false
      })
    },
    hideSinglePost(value: boolean, id: string='') {
      this.singlePost = !value
      this.singlePostId = id
    }
  },
})