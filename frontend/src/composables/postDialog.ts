import { reactive } from "vue"

export function usePostDialog() {
  const state = reactive({
    isOpen: false
  })
  
  function close() {
    state.isOpen = false
  }

  function open() {
    state.isOpen = true
  }

  function postCreated() {
    close()
  }

  function postUpdated() {
    close()
  }

  return {
    state,
    open,
    close,
    postCreated,
    postUpdated
  }
}
