<template>
  <ion-page>
    <ion-content class="ion-text-center" style="height: 100%;">

      <ion-grid>
        <ion-row class="ion-justify-content-center ion-align-items-end" style="height: 100%;">
          <ion-col size="4">

            <!-- Start of login form -->
            <ion-grid>

              <ion-row>
                <ion-col>
                  <ion-title>TBD</ion-title>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-input class="login" fill="outline" v-model="state.username" type="text" placeholder="Username"></ion-input>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-input fill="outline" v-model="state.password" type="password" placeholder="Password"></ion-input>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-button color="primary" expand="block" @click="submitForm()">Login</ion-button>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <a>Forgotten password?</a>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-button color="success" expand="block">Create Account</ion-button>
                </ion-col>
              </ion-row>

            </ion-grid>
            <!-- End of login form -->
            
          </ion-col>
        </ion-row>
      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>

import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonInput, IonLabel, IonButton, IonTitle, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, ref } from 'vue'
import { useMutation } from '@vue/apollo-composable'

const state = reactive({
  username: '',
  password: ''
})

const ionRouter = useIonRouter();

function submitForm () {

  // const { mutate, onDone } = useMutation(gql`    
  //     mutation ($username: String!, $password: String!) {
  //       tokenAuth(username: $username, password: $password) {
  //         success,
  //         errors,
  //         unarchiving,
  //         token,
  //         refreshToken,
  //         unarchiving,
  //         user {
  //           id,
  //           username,
  //         }
  //       }
  //     }

  //   `,{
  //       // Parameters
  //       variables: {
  //         username: state.username,
  //         password: state.password
  //       }
  //     }
  // )

  // mutate()

  // console.log(state.username, state.password)

  // onDone((result) => {
  //   console.log(result.data);
  // })

  ionRouter.push('/category');
}

</script>

<style>
ion-input.login {
  --border-color: var(--ion-color-step-300, #b3b3b3);
  --border-radius: 4px;
  --border-width: 10px;
}
</style>