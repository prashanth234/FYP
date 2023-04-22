import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state () {
    return {
      user: {
        success: false
      },
      toast: {
        message: '',
        open: false,
        color: ''
      },
      auth: {
        open: false
      }
    }
  },
  mutations: {
    storeUser(state, user) {
      state.user = user 
    },
    displayToast(state, toast) {
      state.toast = {...toast, open: true}
    },
    dismissToast(state) {
      state.toast.open = false
    },
    dismissAuth(state) {
      state.auth.open = false
    },
    displayAuth(state) {
      state.auth.open = true
    }
  }
})

export default store