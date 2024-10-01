<template>

  <ion-card class="user-card">

    <ion-row
      class="ion-justify-content-between full-height"
    >

      <ion-col size="12">
        <ion-avatar class="avatar">
          <img
            alt="person"
            :src="userAvatar"
          />
        </ion-avatar>
      </ion-col>

      <ion-col size="12">
        <div class="username two-line-ellipsis"> {{ props.user.username }} </div>
      </ion-col>

      <ion-col size="12">
        <a 
          target="_blank"
          :href="props.files[0]"
          :class="{'disabled': !props.files.length}"
          class="attachements"
        > 
          <ion-icon style="padding-right: 3px;" size="small" :icon="documentAttachOutline"></ion-icon> Attachment 
        </a>
      </ion-col>

      <ion-col size="12" style="display: flex; padding: 0px;">

        <ion-button
          class="ion-no-margin buttons cancel-button"
          size="small"
          color="light"
          expand="full"
          @click="emit('action', false)"
        >
          Ignore
        </ion-button>

        <ion-button
          class="ion-no-margin buttons"
          size="small"
          expand="full"
          @click="emit('action', true)"
        >
          Accept
        </ion-button>

      </ion-col>

    </ion-row>

  </ion-card>

</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { IonAvatar, IonRow, IonCol, IonCard, IonIcon, IonButton } from '@ionic/vue'
import { documentAttachOutline } from 'ionicons/icons'

const props = defineProps(['user', 'files'])
const emit = defineEmits(['action'])

const userAvatar = computed(() => {
  return props.user.avatar || '/static/core/avatar.svg'
})

</script>

<style lang="scss" scoped>
.user-card {
  border-radius: 5px;
  min-height: 194px;
}
.avatar {
  width: 50px;
  height: 50px;
  margin-top: 10px;
  margin-left: auto;
  margin-right: auto;
  border: 0.5px solid gray;
}
.username {
  font-size: 16px;
  font-weight: 580;
  padding: 2px;
  color: var(--ion-color-dark);
}
.buttons {
  flex: 1;
}
.attachements {
  display: inline-flex;
  text-decoration: none;
  margin-bottom: 10px;
}
.disabled {
  color: gray;
  pointer-events: none;
  cursor: not-allowed;
}
</style>