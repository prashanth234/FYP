<template>
  <div class="privacy-terms-links">
    <a @click="navigate('/terms')">Terms</a>
    <span>&middot;</span>
    <a @click="navigate('/privacy')">Privacy</a>
  </div>
</template>


<script lang="ts" setup>
const emit = defineEmits(['onClick'])

function navigate(path: string) {
  emit('onClick')
  window.open(`${window.location.origin}${path}`)
}


</script>

<style lang="scss" scoped>
.privacy-terms-links {
  padding: 5px;
  text-align: center;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: gray;
  flex-wrap: nowrap;
  a {
    padding-right: 10px;
    padding-left: 10px;
    color: gray;
    cursor: pointer;
  }
  a:hover {
    text-decoration: underline;
  }
}
</style>