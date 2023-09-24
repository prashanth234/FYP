import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

export const useUserStore = defineStore('user', {
  state: () => ({ 
    success: false,
    username: '',
    avatar: '',
    points: 0,
    userUpdated: 1,
    email: '',
    firstName: '',
    lastName: '',
    gender: '',
    auth: false
  }),
  getters: {
    
  },
  actions: {
    getDetails() {
      const { result, onResult } = useQuery(gql`   
                                  query me {
                                    me {
                                      username,
                                      firstName,
                                      lastName,
                                      email,
                                      gender,
                                      avatar,
                                      points
                                    }
                                  }
                                `)
      
      onResult(({data, loading}) => {
        if (loading) return
        if (data.me) {
          this.$patch({...data.me, userUpdated: this.userUpdated + 1})
        } else {
          this.reset()
        }
      })
    },
    reset() {
      localStorage.removeItem('fyptoken')
      localStorage.removeItem('fyprefreshtoken')
      this.$reset()
    }
  }
})