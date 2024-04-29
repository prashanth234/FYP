<template>
  <div class="social-icons">
    <a
      v-for="(link, social, index) in links" :key="index"
      :href="link"
      target="_blank"
      v-show="link"
    >
      <ion-icon :icon="icons[social]" :style="`color: ${props.color}; font-size: ${props.size}px`"></ion-icon>
    </a>
  </div>
</template>


<script lang="ts" setup>
import { mailOutline, logoFacebook, logoInstagram, logoLinkedin, logoWhatsapp } from 'ionicons/icons'
import { IonIcon } from '@ionic/vue';
import { reactive } from 'vue';

const props = defineProps({
  orglinks: {
    type: Boolean,
    default: false
  },
  size: String,
  color: String,
  instagram: String,
  facebook: String,
  whatsapp: String,
  linkedin: String,
  mail: String
})

const icons = reactive({
  instagram: logoInstagram,
  facebook: logoFacebook,
  whatsapp: logoWhatsapp,
  linkedin: logoLinkedin,
  mail: mailOutline
})

const orglinks = {
  instagram: 'https://www.instagram.com/_selfdive/',
  facebook: 'https://www.facebook.com/profile.php?id=61556241308978&mibextid=LQQJ4d',
  whatsapp: 'https://wa.me/+919494990138',
  linkedin: 'https://www.linkedin.com/company/selfdive/',
  mail: 'mailto:support@selfdive.com'
}

const links = reactive(props.orglinks ? orglinks : {
  instagram: props.instagram,
  facebook: props.facebook,
  whatsapp: props.whatsapp,
  linkedin: props.linkedin,
  mail: props.mail
})
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
  :last-of-type ion-icon {
    margin-right: 0px;
  }
}
</style>