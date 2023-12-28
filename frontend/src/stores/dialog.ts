import { defineStore } from 'pinia'

export interface Button {
    title: string,
    color: string,
    action?: string,
    control?: any
}

interface State {
    open: boolean, 
    title: string,
    description: string,
    icon: string,
    iconColor: string,
    buttons: Array<Button>
} 

export const useDialogStore = defineStore('dialog', {
  state: () => (<State>{ 
    open: false,
    title: '',
    description: '',
    icon: '',
    iconColor: '',
    buttons: [],
  }),
  getters: {
  },
  actions: {
    show(title: string, description: string, buttons: Array<Button>, icon?: string, iconColor?: string) {
      this.$patch({title, description, buttons, icon, iconColor, open: true})
    },
    close() {
      this.$reset()
      // this.open = false
    }
  },
})