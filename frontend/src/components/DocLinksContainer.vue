<template>
  <div class="privacy-terms-links">
    <a target="_blank" href="/terms">Terms</a>
    <span>&middot;</span>
    <a target="_blank" href="/privacy">Privacy</a>
  </div>
</template>


<script lang="ts" setup>
// const emit = defineEmits(['onClick'])

// function navigate(path: string) {
//   emit('onClick')
// }
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