<template>
  <ion-page>
    <ion-content class="full-height" ref="content">
      <ion-row class="ion-justify-content-center ion-margin-top">
        <ion-col size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8">
          <post v-if="state.postDetails" :post="state.postDetails"></post>
          <div class="ion-margin-vertical ion-text-center ion-padding-vertical">
            <ion-button fill="clear" @click="discoverMore">Click to discover more posts</ion-button>
          </div>
        </ion-col>
      </ion-row>
  </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { reactive } from 'vue'
import { getPostDetails } from '@/composables/posts'
import { useToastStore } from '@/stores/toast'
import Post from '@/components/PostContainer.vue'
import { Post as PostType } from '@/utils/interfaces'
import { IonButton, useIonRouter, IonPage, IonContent, IonRow, IonCol } from '@ionic/vue';

const props = defineProps({
  id: String,
  postid: String
})

interface State {
  postDetails: PostType | null
}

const state: State = reactive({
  postDetails: null
})

const route = useRoute();
const toast = useToastStore();
const ionRouter = useIonRouter();

fetchPostDetails()

// Get indivual post details if searched for a post using postid
function fetchPostDetails () {
  if (props.postid) {
    state.postDetails = null
    const { onResult, onError } = getPostDetails(props.postid, '1')
    onResult(({data, loading}) => {
      !loading && (state.postDetails = data.postDetails)
    })
    onError((error) => {
      if (error?.graphQLErrors) {
        toast.$patch({message: error?.graphQLErrors[0].message, color: 'danger', open: true})
      } else {
        toast.$patch({message: 'Post retrieval error. Please Retry.', color: 'danger', open: true})
      }
    })
  }
}

function discoverMore() {
  state.postDetails && ionRouter.push(`/interests/${state.postDetails.category.id}`)
}

</script>