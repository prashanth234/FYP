import { defineStore } from 'pinia'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

export const useUserStore = defineStore('user', {
  state: () => ({ 
    success: false,
    token: '',
    refreshToken: '',
    username: '',
    avatar: '',
    points: 0,
    userUpdated: 1,
    email: '',
    phone: '',
    firstName: '',
    lastName: '',
    gender: '',
    verified: false,
    auth: false,
    authMessage: ''
  }),
  getters: {
    
  },
  actions: {
    getAvatar() {
      const { onResult } = useQuery(gql`   
                                  query user {
                                    user {
                                      avatar,
                                      id
                                    }
                                  }
                                `)
      
      onResult(({data, loading}) => {
        if (loading) return
        this.$patch({avatar: data.user?.avatar, userUpdated: this.userUpdated + 1})
      })
    },
    getDetails() {
      // Also change in loginformcontainer.vue user query
      const { result, onResult } = useQuery(gql`   
                                  query me {
                                    me {
                                      username,
                                      firstName,
                                      lastName,
                                      email,
                                      phone,
                                      gender,
                                      points,
                                      verified
                                    }
                                  }
                                `, null, {
                                  fetchPolicy: "no-cache"
                                })
      
      onResult(({data, loading}) => {
        if (loading) return
        if (data.me) {
          this.$patch({...data.me, userUpdated: this.userUpdated + 1})
        } else {
          this.reset()
        }
      })

      this.getAvatar()
    },
    reset() {
      localStorage.removeItem('fyptoken')
      localStorage.removeItem('fyprefreshtoken')
      this.$reset()
    }
  }
})