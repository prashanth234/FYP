<template>
  <ion-toast
    position="top"
    :color="store.state.toast.color"
    :is-open="store.state.toast.open"
    :message="store.state.toast.message"
    :duration="5000"
    @didDismiss="store.commit('dismissToast')"
    :buttons="toastButtons"
  ></ion-toast>
</template>

<script lang="ts" setup>

import store from '@/vuex'
import { IonToast } from '@ionic/vue'
import { ref } from 'vue'
// import { closeOutline } from 'ionicons/icons'

const toastButtons = ref([
        {
          text: 'Dismiss',
          role: 'cancel'
        }
      ])

</script>

<style scoped>
ion-toast.custom-toast {
  --background: #F4F4FA;
  --box-shadow: 3px 3px 10px 0 rgba(0, 0, 0, 0.2);
  --color: #4b4a50;
}
  
ion-toast.custom-toast::part(message) {
  font-style: italic;
}

ion-toast.custom-toast::part(button) {
  border-left: 1px solid #d2d2d2;
  color: #030207;
  font-size: 15px;
}
</style>