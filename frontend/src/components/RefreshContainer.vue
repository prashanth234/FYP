<template>

  <div class="refresh-icon cpointer ion-hide-sm-down">
    <Refresh 
      @click="emit('refresh')"
      width="22px"
      height="22px"
    />
  </div>

  <Transition name="fade">
    <div
      class="ion-hide-sm-down"
      v-if="props.refreshing"
      style="padding-left: 5px; color: var(--ion-color-primary)">Refreshing...
    </div>
  </Transition>

</template>

<script lang="ts" setup>
import Refresh from '@/components/icons/refresh.vue'

const props = defineProps({
  refreshing: Boolean
})

const emit = defineEmits(['refresh'])

</script>

<style lang="scss">

.refresh-icon {
  margin-left: 5px;
  margin-top: 1px;
  height: 22px;
  width: 22px;
  opacity: 0.9;
  &:hover {
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>