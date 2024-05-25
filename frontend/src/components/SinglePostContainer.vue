<template>

  <div v-if="!loading">
    <post v-if="post" :post="post.postDetails"/>
    <div class="ion-margin-vertical ion-text-center ion-padding-vertical">
      <ion-button fill="clear" @click="morePosts">Click to discover more posts</ion-button>
    </div>
  </div>

</template>

<script lang="ts" setup>
import { IonButton, useIonRouter } from '@ionic/vue'
import { getPostDetails } from '@/composables/posts'
import Post from '@/components/PostContainer.vue'
import { useRoute } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const ionRouter = useIonRouter()
const router = useRoute()

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  category: String,
  entity: String
})

const emit = defineEmits(['more'])

// Get indivual post details if searched using url
const { post, onError, loading } = getPostDetails(props.id, props.category, props.entity)

onError((error) => {
  if (error?.graphQLErrors) {
    if (error?.graphQLErrors[0].message == 'NOTFOUND') {
      showDanger('Post not found.')
    }
  } else {
    showDanger('Post retrieval error. Please Retry.')
  }
})

function showDanger(message: string) {
  toast.$patch({message: message, color: 'danger', open: true})
  ionRouter.replace({name: router.name, params: { id: router.meta.id }})
}

function morePosts() {
  emit('more')
}

</script>

<style lang="scss">

</style>