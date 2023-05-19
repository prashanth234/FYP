<template>
  <ion-card class="border-radius-std post-card cpointer">
    <ion-card-content @click="likePost()" class="padding-zero">
      <ion-list>
        <ion-item lines="full">
          <ion-avatar slot="start">
            <img alt="Silhouette of a person's head" src="https://ionicframework.com/docs/img/demos/avatar.svg" />
          </ion-avatar>
          <ion-label>{{ post.user.username }}</ion-label>
          <ion-icon v-if="props.showEdit" @click="emit('editPost')" class="cpointer edit operations" :icon="pencilOutline"></ion-icon>
          <ion-icon v-if="props.showEdit" @click="emit('deletePost')" class="cpointer delete operations" :icon="trashOutline"></ion-icon>
        </ion-item>
        <ion-item lines="none" style="padding-top: 20px; padding-bottom: 20px">
          <ion-img class="ml-auto mr-auto" :src="`${ [post.postfileSet[0].file] }`" alt="Image"></ion-img>
        </ion-item>
        <ion-item lines="full">
          <p>{{ post.description }}</p>
        </ion-item>
        <ion-item lines="none">
          <ion-icon v-if="state.isliked" style="color:red" :icon="heart" size="large"></ion-icon>
          <ion-icon v-else :icon="heartOutline" size="large"></ion-icon>
          <ion-label class="ion-padding-start">{{ state.likeCount }} Like{{state.likeCount == 1 ? '' : 's'}}</ion-label>
        </ion-item>
      </ion-list>
    </ion-card-content>
  </ion-card>
</template>

<script lang="ts" setup>
import { IonList, IonItem, IonImg, IonLabel, IonAvatar, IonCard, IonCardContent, IonPopover, IonContent, IonIcon, useIonRouter  } from '@ionic/vue';
import { heartOutline, heart, pencilOutline, trashOutline } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import store from '@/vuex'
import gql from 'graphql-tag'
import { reactive } from 'vue'

const ionRouter = useIonRouter()
const props = defineProps(['post', 'showEdit'])

const emit = defineEmits<{
  (e: 'editPost'): void
  (e: 'deletePost'): void
}>()

const state = reactive({
  isliked: props.post.userLiked,
  likeCount: props.post.likeCount
})

function likePost () {

  if (!store.state.user.success) {
    store.commit('displayAuth')
    return
  }

  const operation = state.isliked ? 'unlikeItem' : 'likeItem'
  state.isliked ? state.likeCount-- : state.likeCount++
  state.isliked = !state.isliked
 

  const { mutate, onDone } = useMutation(gql`    
      
      mutation ($id: ID!) { 
        ${operation} (id: $id) {
          success
        }
      }

    `, {
        // Parameters
        variables: {
          id: parseInt(props.post.id)
        }
      }
    )

    mutate()
}

</script>

<style scoped>

/* Edit and delete operations */
.edit {
  margin-right: 10px;
}
.edit:hover {
  color: var(--ion-color-primary);
  border-color: var(--ion-color-primary);
}
.delete:hover {
  color: var(--ion-color-danger);
  border-color: var(--ion-color-danger);
}
.operations {
  font-size: 16px;
  padding: 9px;
  border: 1px solid grey;
  border-radius: 30px;
  opacity: 0.5;
}
.operations:hover {
  border-width: 2px;
  opacity: 1;
}
.post-card {
  transition: all;
  transition-timing-function: ease-out;
}
.post-card:hover {
  box-shadow: 0 2px 4px -1px rgba(0,0,0,.2),0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12)!important;
}
.post-card:hover ion-icon {
  color: red;
}
</style>