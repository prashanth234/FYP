<template>

  <div class="alert" :class="`alert-${props.type}`">
    <ion-icon v-if="showIcon" class="icon" :icon="icons[props.type]"></ion-icon>
    {{ props.message }}
  </div>

</template>

<script lang="ts" setup>
import { informationCircleOutline, checkmarkCircleOutline, warningOutline, closeCircleOutline } from 'ionicons/icons'
import { reactive } from 'vue';

const props = defineProps({
  message: String,
  type: {
    type: String,
    required: true
  },
  showIcon: {
    type: Boolean,
    default: false
  }
})

interface Icons {
  success: any,
  warning: any,
  error: any,
  info: any,
  [key: string]: any
}

const icons: Icons = reactive({
  success: checkmarkCircleOutline,
  warning: warningOutline,
  error: closeCircleOutline,
  info: informationCircleOutline
})

</script>

<style lang="scss">
  .alert {
    font-weight: 500;
    padding: 10px;
    font-size: 15px;
    border-radius: 5px;
    border-width: 0.1px;
    border-style: solid;
    .icon {
      margin-top: auto;
      margin-bottom: auto;
      margin-right: 5px;
      font-size: 20px;
    }
  }

  .alert-success {
    background-color: var(--alert-bg-success);
    color: var(--ion-color-success-shade);
    border-color: var(--ion-color-success);
  }

  .alert-warning {
    background-color: var(--alert-bg-warning);
    color: var(--ion-color-warning-shade);
    border-color: var(--ion-color-warning);
  }

  .alert-info {
    background-color: var(--alert-bg-info);
    color: var(--ion-color-primary);
    border-color: var(--ion-color-primary);
  }

  .alert-error {
    background-color: var(--alert-bg-error);
    color: var(--ion-color-danger);
    border-color: var(--ion-color-danger);
  }
</style>