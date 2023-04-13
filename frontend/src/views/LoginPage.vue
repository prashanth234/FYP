<template>
  <ion-page>
    <ion-content class="ion-text-center" style="height: 100%;">
      
      <ion-grid>
        <ion-row class="ion-justify-content-center ion-align-items-end" style="height: 100%;">
          <ion-col size="3">

            <ion-card>
              <ion-card-content>

                <!-- Start of login form -->
                <ion-grid>

                  <ion-row>
                    <ion-col>
                      <ion-title>TBD</ion-title>
                    </ion-col>
                  </ion-row>

                  <ion-row>
                    <ion-col>
                      <ion-input class="custom-input" fill="outline" v-model="state.username" type="text" placeholder="Username"></ion-input>
                    </ion-col>
                  </ion-row>

                  <ion-row>
                    <ion-col>
                      <ion-input class="custom-input" fill="outline" v-model="state.password" type="password" placeholder="Password"></ion-input>
                    </ion-col>
                  </ion-row>

                  <ion-row class="danger" v-if="state.errors.length">
                    <ion-col>
                      <ion-text color="danger">
                        <ul style="padding-left: 15px">
                          <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
                        </ul>
                      </ion-text>
                    </ion-col>
                  </ion-row>

                  <ion-row>
                    <ion-col>
                      <ion-button color="primary" :disabled="state.disabled" expand="block" @click="submitForm()">Login</ion-button>
                    </ion-col>
                  </ion-row>

                  <ion-row>
                    <ion-col>
                      <a>Forgotten password?</a>
                    </ion-col>
                  </ion-row>

                  <ion-row>
                    <ion-col>
                      <ion-button :disabled="state.disabled" size="small" color="success" @click="register()">Create Account</ion-button>
                    </ion-col>
                  </ion-row>

                </ion-grid>
                <!-- End of login form -->

              </ion-card-content>
            
            </ion-card>

          </ion-col>
        </ion-row>
      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>

import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonInput, IonCard, IonCardContent, IonButton, IonTitle, IonText, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, ref } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import store from '@/vuex'

const state = reactive({
  username: '',
  password: '',
  disabled: false,
  errors: []
})

const ionRouter = useIonRouter();

function submitForm () {

  state.disabled = true

  const { mutate, onDone } = useMutation(gql`    
      mutation ($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
          success,
          errors,
          unarchiving,
          token,
          refreshToken,
          unarchiving,
          user {
            id,
            username,
          }
        }
      }

    `,{
        // Parameters
        variables: {
          username: state.username,
          password: state.password
        }
      }
  )

  mutate()

  onDone((result) => {
    const response = result.data.tokenAuth
    state.disabled = false

    if (response.success) {
      localStorage.setItem('fyptoken', response.token)
      localStorage.setItem('fyprefreshtoken', response.refreshToken)
      store.commit('storeUser', response)
      ionRouter.push('/')
    } else {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}) => {
          state.errors.push(message)
        })
      })
    }
  })
}

function register() {
  ionRouter.push('/register')
}

</script>