import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { CategoryType } from '@/utils/interfaces'

export const useCategoryStore = defineStore('category', {
  state: () => ({ 
    categories: [] as CategoryType[],
    loading: false
  }),
  getters: {
  },
  actions: {
    getCategories () {
      if (this.categories.length) { return }
      this.loading = true
      const { result, onResult, onError } = useQuery(gql`
                              query categories {
                                categories {
                                  name,
                                  description,
                                  id,
                                  image,
                                  oftype,
                                  key
                                }
                              }
                            `)

      onResult(({data, loading}) => {
        // console.log(data, loading)
        if (!loading) {
          this.categories = data.categories
          this.loading = false
        }
      })

      onError(() => {
        this.loading = false
      })
    }
  },
})