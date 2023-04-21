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
      }
    }
  },
  mutations: {
    storeUser (state, user) {
      state.user = user 
    },
    displayToast(state, toast) {
      state.toast = {...toast, open: true}
    },
    dismissToast(state) {
      state.toast.open = false
    }
  }
})

export default store