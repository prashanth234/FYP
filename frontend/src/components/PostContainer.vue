<template>
  <ion-card class="border-radius-std">
    <ion-card-content @dblclick="likePost()">
      <ion-list lines="none">
        <ion-item>
          <ion-avatar slot="start">
            <img alt="Silhouette of a person's head" src="https://ionicframework.com/docs/img/demos/avatar.svg" />
          </ion-avatar>
          <ion-label>{{ post.user.username }}</ion-label>
          <ion-icon v-if="props.showEdit" @click="emit('editPost')" class="cpointer edit operations" :icon="pencilOutline"></ion-icon>
          <ion-icon v-if="props.showEdit" @click="emit('deletePost')" class="cpointer delete operations" :icon="trashOutline"></ion-icon>
        </ion-item>
        <ion-item style="padding-top: 20px; padding-bottom: 20px">
          <ion-img :src="`${ [post.postfileSet[0].file] }`" alt="Image"></ion-img>
        </ion-item>
        <ion-item>
          <p>{{ post.description }}</p>
        </ion-item>
        <ion-item>
          <ion-icon v-if="state.isliked" color="danger" :icon="heart" size="large"></ion-icon>
          <ion-icon v-else :icon="heartOutline" size="large"></ion-icon>
          <ion-label class="ion-padding">{{ state.likeCount }} Like{{state.likeCount == 1 ? '' : 's'}}</ion-label>
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
</style>