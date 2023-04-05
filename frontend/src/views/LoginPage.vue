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
                  <ion-title>Login</ion-title>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-input label="Username" label-placement="floating" fill="outline" v-model="state.username" type="text" placeholder="Enter your username"></ion-input>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-input label="Password" label-placement="floating" fill="outline" v-model="state.password" type="password" placeholder="Enter your password"></ion-input>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-button @click="submitForm()">Submit</ion-button>
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

<!-- <script>


export default {
  name: 'LoginForm',
  components: {
      IonPage,
      IonContent,
      IonCol,
      IonGrid,
      IonRow,
      IonInput,
      IonButton,
      IonTitle
  },
  data () {
      return {
          username: '',
          password: ''
      }
  },
  methods: {
      submitForm () {
        const ionRouter = useIonRouter();
        ionRouter.push('/category');

        // this.$router.push('/category')
        return
        this.$apollo.mutate({
          // Query
          mutation: gql`
          
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

          `,
          // Parameters
          variables: {
            username: this.username,
            password: this.password
          }
        }).then((data) => {
          // Result
          this.$store.commit('storeUser', data.data.tokenAuth)
          this.$router.push('/category')
        }).catch((error) => {
          // Error
          console.error(error)
        })
      },
  },
};  
</script> -->