<template>
  <div class="privacy-terms-links">
    <a @click="navigate('/terms')">Terms</a>
    <span>&middot;</span>
    <a @click="navigate('/privacy')">Privacy</a>
  </div>
</template>


<script lang="ts" setup>
import { useIonRouter } from '@ionic/vue';
const ionRouter = useIonRouter();

const emit = defineEmits(['onClick'])

function navigate(path: string) {
  emit('onClick')
  ionRouter.push(path)
}


</script>

<style lang="scss" scoped>
.privacy-terms-links {
  padding: 10px;
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