<template>
  
  <ion-list>

    <ion-item>
      <ion-input v-model="state.oldPassword" type="password" label="Old Password" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="state.newPassword1" type="password" label="New Password" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="state.newPassword2" type="password" label="Confirm Password" labelPlacement="floating"></ion-input>
    </ion-item>
    
    <ion-item v-if="state.errors.length" lines="none">
      <ion-text color="danger">
        <ul style="padding-left: 15px">
          <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
        </ul>
      </ion-text>
    </ion-item>

  </ion-list>

  <ion-row>
    <ion-col size="12">
      <ion-button
        color="primary"
        class="float-right"
        size="small"
        @click="changePassword"
        :disabled="state.loading"
      >
        <ion-spinner 
          class="button-loading-small"
          v-if="state.loading"
          name="crescent"
        />
        <span v-else>
          Update
        </span>
      </ion-button>
      <ion-button
        color="light"
        @click="clear"
        class="float-right"
        style="margin-right: 15px;"
        :disabled="state.loading"
        size="small"
      >
        Clear
      </ion-button>
    </ion-col>
  </ion-row>

</template>

<script setup lang="ts">
import { IonList, IonItem, IonInput, IonRow, IonCol, IonText, IonButton, IonSpinner } from '@ionic/vue'
import { reactive } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useToastStore } from '@/stores/toast'

interface State {
  oldPassword: string,
  newPassword1: string,
  newPassword2: string,
  errors: string[],
  loading: boolean
}

const state:State = reactive({
  oldPassword: '',
  newPassword1: '',
  newPassword2: '',
  errors: [],
  loading: false
})

const toast = useToastStore()

function clear () {
  state.newPassword1 = ''
  state.newPassword2 = ''
  state.oldPassword = ''
  state.errors = []
}

function changePassword () {
  const {oldPassword, newPassword1, newPassword2} = state

  state.loading = true

  try {
    const { mutate, onDone } = useMutation(gql`
      mutation ($oldPassword: String!, $newPassword1: String!, $newPassword2: String!)  {
        passwordChange(
            oldPassword: $oldPassword,
            newPassword1: $newPassword1,
            newPassword2: $newPassword2
          ) {
            success,
            errors,
            token,
            refreshToken
          }
      }
    `,
      {
        variables: {
          oldPassword,
          newPassword1,
          newPassword2
        },
      }
    )
    mutate()
    onDone((result) => {
      const response = result.data.passwordChange

      if (response.success) {
        toast.$patch({message: 'Password Changed Successfully', color: 'success', open: true})
        clear()
      } else {
        const keys = Object.keys(response.errors)
        state.errors = []
        keys.forEach(key => {
          response.errors[key].forEach(({message}:{message: string}) => {
            state.errors.push(message)
          })
        })
      }

      state.loading = false
    })
  } catch (error) {
    console.error(error)
    state.loading = false
  }
}

</script>

<style lang="scss" scoped>
</style>