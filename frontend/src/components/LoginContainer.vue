<template>

  <ion-card>

      <ion-row>

        <ion-col size ="6" class="login-background">

          <ion-row class="fyp-intro ion-align-items-start">
            
            <ion-col size="12">

              <ion-row>
                <ion-col size="auto" style="margin: auto; margin-top: 30px; margin-bottom: 10px;">
                  <ion-img class="fyp-logo" src="http://localhost:8000/static/logo.png"></ion-img>
                </ion-col>
                <ion-col class="fyp-start-title" size="12">
                  Start Your Journey With Us
                </ion-col>
                <ion-col class="fyp-start-description" size="10">
                  Discover the Power of Passion with Us. We are here to help you.
                </ion-col>
              </ion-row>

            </ion-col>

          </ion-row>

        </ion-col>

        <ion-col size="5" style="align-self: center; margin: auto">
          <login-form-container v-if="state.login" @register="changeContainer"></login-form-container>
          <register-form-container v-else @login="changeContainer"></register-form-container>
        </ion-col>

      </ion-row>
      
  </ion-card>

</template>

<script lang="ts" setup>
import { IonCol, IonRow, IonCard, IonImg } from '@ionic/vue';
import { reactive } from 'vue';
import LoginFormContainer from './LoginFormContainer.vue';
import RegisterFormContainer from './RegisterFormContainer.vue';

const state = reactive({
  login: true
})

function changeContainer () {
  state.login = !state.login
}
</script>

<style>
.login-background {
  background: linear-gradient(158.37deg, #1D5FE4 50.52%, rgba(106, 149, 236, 0.807566) 82.71%);
  height: 450px;
}
.fyp-intro {
  color: #FFFFFF;
  text-align: start;
  height: 100%;
}
.fyp-start-title {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-size: 30px;
  line-height: 44px;
}
.fyp-start-description {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 200;
  font-size: 20px;
  line-height: 24px;
}
.fyp-logo {
  width: 67px;
  height: 33px;
}
</style>