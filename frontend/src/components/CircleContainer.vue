<template>

  <div class="main">

    <div class="circle" :style="`border-color: var(--ion-color-secondary-tint)`">
      {{ props.count }}
    </div>

    <div class="label ion-text-center">
      {{ props.label }}
    </div>

  </div>

  

</template>

<script lang="ts" setup>
const props = defineProps({
  count: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  color: {
    type: String,
    required: true
  }
})
</script>

<style lang="scss">

.main {
  .circle {
    border-width: 5px;
    border-style: solid;
    height: 50px;
    width: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 590;
    font-size: 18px;
    margin: 0px auto;
  }
  .label {
    font-size: 16px;
    font-weight: 590;
    margin-top: 5px;
    text-wrap: nowrap;
  }
}

</style>