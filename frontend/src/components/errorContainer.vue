<template>
  <TransitionGroup name="list" tag="ul" class="ul-error-text" :class="{'no-space': props.nospace && !props.errors.length}">
    <li v-for="(message, index) in props.errors" :key="index">
      {{ message }}
    </li>
  </TransitionGroup>
</template>

<script lang="ts" setup>
  const props = defineProps<{
    errors: string[],
    nospace?: boolean
  }>()
</script>

<style scoped>
  .ul-error-text {
    padding-left: 20px;
    font-size: 14px;
    text-align: start;
    color: var(--ion-color-danger);
  }
  .list-enter-active,
  .list-leave-active {
    transition: all 0.5s ease;
  }
  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: translateX(30px);
  }
  .no-space {
    margin: 0px;
  }
</style>