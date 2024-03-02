<template>
  <div class="social-icons mr-auto ml-auto">
    <a href="https://www.instagram.com/_selfdive/" target="_blank">
      <ion-icon  :icon="logoInstagram"></ion-icon>
    </a>
    <a href="https://www.linkedin.com/company/selfdive/" target="_blank">
      <ion-icon  :icon="logoLinkedin"></ion-icon>
    </a>
    <a href="https://www.facebook.com/profile.php?id=61556241308978&mibextid=LQQJ4d" target="_blank">
      <ion-icon  :icon="logoFacebook"></ion-icon>
    </a>
    <a  href="https://wa.me/+919494990138" target="_blank">
      <ion-icon :icon="logoWhatsapp"></ion-icon>
    </a>
    <a href="mailto:support@selfdive.com" target="_blank">
      <ion-icon class="last" :icon="mailOutline"></ion-icon>
    </a>
  </div>
</template>


<script lang="ts" setup>
import { mailOutline, logoFacebook, logoInstagram, logoLinkedin, logoWhatsapp } from 'ionicons/icons'
import { IonIcon } from '@ionic/vue';
</script>

<style lang="scss" scoped>
.social-icons {
  display: flex;
  padding: 5px;
  a {
    cursor: pointer;
    color: var(--ion-color-dark);
  }
  ion-icon {
    font-size: 22px;
    margin-right: 15px;
  }
  .last {
    margin-right: 0px;
  }
}
</style>