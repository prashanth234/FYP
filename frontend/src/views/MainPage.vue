<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-grid>
          <ion-row class="ion-align-items-center">
            <ion-col>
              <ion-title>TBD</ion-title>
            </ion-col>
            <ion-col size="auto" v-if="store.state.user.success">
              <ion-icon class="icon-custom cpointer" :icon="logOutOutline" @click="logout()"></ion-icon>
            </ion-col>
            <ion-col size="auto" class="ion-padding-end" v-else>
              <ion-button @click="login()">Login</ion-button>
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-modal :show-backdrop="true" :is-open="store.state.auth.open" @didDismiss="closeLogin">
        <ion-icon @click="closeLogin" class="close-login" size="large" :icon="closeOutline"></ion-icon>
        <login-container />
      </ion-modal>
      <ion-router-outlet></ion-router-outlet>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow, useIonRouter } from '@ionic/vue';
import { logOutOutline } from 'ionicons/icons'
import store from '@/vuex'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens } from '@/mixims/auth'
import { closeOutline } from 'ionicons/icons'
import LoginContainer from '@/components/LoginContainer.vue'

const ionRouter = useIonRouter();

function logout() {
  localStorage.removeItem('fyptoken')
  localStorage.removeItem('fyprefreshtoken')
  store.commit('storeUser', {})
}

function closeLogin() {
  store.commit('dismissAuth')
}

function login() {
  store.commit('displayAuth')
  // ionRouter.push('/login')
}

function checkAuthStatus() {
  if (store.state.user.success) { return }

  const token = localStorage.getItem('fyptoken')

  if (token) {

    // Verify if the token is vaild or not
    const { mutate, onDone } = useMutation(gql`
      mutation ($token: String!) {
          verifyToken (
            token: $token
          ) {
            success,
            errors,
            payload
          }
        }
      `,
      {
        variables: {
          token
        }
      }
    )

    mutate()

    onDone(({data: {verifyToken}}) => {
      const refreshToken = localStorage.getItem('fyprefreshtoken')

      if (verifyToken.success) {
        const user = { username: verifyToken.payload.username, token, refreshToken, success: true }
        store.commit('storeUser', user)
      } else {
        // If not vaild, refresh the token
        const { mutate, onDone } = useMutation(gql`
          mutation ($refreshToken: String!) {
              refreshToken (
                refreshToken: $refreshToken
              ) {
                success,
                errors,
                payload,
                token,
                refreshToken
              }
            }
          `,
          {
            variables: {
              refreshToken
            }
          }
        )

        mutate()

        onDone(({data: {refreshToken}}) => {
          storeTokens(refreshToken, 'refresh')
        })
      }
    })
  }
}

checkAuthStatus()

</script>

<style scoped>
  .icon-custom {
    padding-right: 15px;
  }
  ion-grid {
    --ion-grid-padding: 0px;
    padding-top: 5px;
    font-size: 25px !important;
  }
  ion-modal {
    --background: transparent;
    --backdrop-opacity: 70%;
    --border-radius: 5px;
    --box-shadow: 0px;
    --height: auto;
  }
  .close-login {
    float: right;
    color: white;
    cursor: pointer;
    line-height: 1;
    vertical-align: top;
    z-index: 5;
  }
</style>