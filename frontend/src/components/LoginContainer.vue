<template>

  <div class="auth-container">
    <Transition name="slide-side" mode="out-in">
      <div v-if="auth.form == 'login'">
        <LoginForm />
      </div>
      <div v-else-if="auth.form == 'register'">
        <RegisterForm />
      </div>
      <div v-else-if="auth.form == 'changepassword'">
        <ChangePassword />
      </div>
      <div v-else-if="auth.form == 'verify'">
        <OtpVerifier />
      </div>
    </Transition>
  </div>

  <!-- <ion-card>
    
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
      
  </ion-card> -->

</template>

<script lang="ts" setup>
import LoginForm from './LoginFormContainer.vue';
import RegisterForm from './RegisterFormContainer.vue';
import ChangePassword from '@/components/ChangePasswordContainer.vue';
import OtpVerifier from './OTPContainer.vue';
import { useAuthStore } from '@/stores/auth';
  
const auth = useAuthStore();
</script>

<style>
.auth-container {
  padding: 35px;
}
.login-background {
  background-image: linear-gradient(314deg, #09c6f9 0%, #045de9 75%);
  height: 450px;
}
.fyp-intro {
  color: #FFFFFF;
  text-align: start;
  height: 100%;
}
.fyp-start-title {
  font-weight: 700;
  font-size: 25px;
  line-height: 44px;
}
.fyp-start-description {
  font-weight: 200;
  font-size: 17px;
  line-height: 24px;
}
.fyp-logo {
  width: 67px;
  height: 33px;
}
.slide-side-enter-active,
  .slide-side-leave-active {
    transition: all 0.25s ease-out;
  }

  .slide-side-enter-from {
    opacity: 0;
    transform: translateX(-30px);
  }

  .slide-side-leave-to {
    opacity: 0;
    transform: translateX(30px);
  }
</style>