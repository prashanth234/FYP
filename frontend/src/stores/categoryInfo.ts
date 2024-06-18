import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CompetitionType, CategoryType, TabSelectedType } from '@/utils/interfaces'
import { RouteLocationNormalizedLoaded } from 'vue-router'

// This store stores information about a openend category, through out the app



export const useCategoryInfoStore = defineStore('categoryInfo', {
  state: () => ({
    type: 'category',
    routeName: 'CategoryDetails',
    queryType: 'allPosts',
    details: {} as CategoryType,
    loading: true,
    selectedComptn: null as CompetitionType | null,
    tabSelected: 'allposts' as TabSelectedType,
    refreshing: false,
    singlePost: false,
    singlePostId: ''
  }),
  getters: {
    getSinglePostParams(state) {
      return {category: state.details.id, id: state.singlePostId }
    }
  },
  actions: {
    getDetails(id: string, route: RouteLocationNormalizedLoaded) {
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
          if (route.params.id == id) {
            this.$patch({details: value.data.categoryDetails})
          }
          this.loading = false
        }
      })

      onError((error) => {
        // ionRouter?.replace('/')
        
      })
    },
    hideSinglePost(value: boolean, id: string='') {
      this.singlePost = !value
      this.singlePostId = id
    }
  },
})