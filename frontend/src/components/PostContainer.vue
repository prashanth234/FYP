<template>
  <ion-card class="border-radius-std post-card cpointer">

    <ion-card-content @dblclick="likePost()" class="ion-no-padding">
      <ion-list class="ion-no-padding">

        <ion-item lines="none" class="line" style="padding: 5px 0px;">
          <ion-avatar slot="start" style="margin: 0px 10px 0px 0px">
            <img
              alt="avatar"
              :src="userAvatar"
            />
          </ion-avatar>
          <ion-label>
            {{ post.user.username }}
          </ion-label>
          <ion-icon
            v-if="props.showEdit"
            @click.stop="emit('editPost')"
            class="cpointer edit operations"
            :icon="pencilOutline"
          />
          <ion-icon 
            v-if="props.showEdit"
            @click.stop="emit('deletePost')"
            class="cpointer delete operations"
            :icon="trashOutline"
          />
        </ion-item>

        <ion-item class="image" lines="none" style="padding-top: 12px;" v-if="post.postfileSet.length">
          <ion-img 
            class="ml-auto mr-auto"
            :src="`/media/${post.postfileSet[0].file}`"
            alt="Image"
          />
        </ion-item>

        <ion-item v-if="post.description" lines="none" style="padding-top: 12px; padding-left: 5px">
          <p>{{ post.description }}</p>
        </ion-item>

        <ion-item lines="none" class="line-top" style="padding: 3px 0px;">
          <ion-icon
            @click="likePost()"
            v-if="post.userLiked"
            style="color:rgb(246, 73, 73)"
            :icon="heart"
            size="large"
          />
          <ion-icon
            @click="likePost()"
            class="like-icon"
            v-else
            :icon="heartOutline"
            size="large"
          />
          <ion-label 
            class="ion-padding-start"
          >
            {{ post.likes }} Like{{post.likes == 1 ? '' : 's'}}
          </ion-label>
        </ion-item>

      </ion-list>
    </ion-card-content>

  </ion-card>
</template>

<script lang="ts" setup>
import { IonList, IonItem, IonImg, IonLabel, IonAvatar, IonCard, IonCardContent, IonIcon, useIonRouter  } from '@ionic/vue';
import { heartOutline, heart, pencilOutline, trashOutline } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import store from '@/vuex'
import gql from 'graphql-tag'
import { reactive, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

const user = useUserStore()
const toast = useToastStore()

const ionRouter = useIonRouter()
const props = defineProps(['post', 'showEdit'])

const emit = defineEmits<{
  (e: 'editPost'): void
  (e: 'deletePost'): void
}>()

const userAvatar = computed(() => {
  return props.post.user.avatar ? `/media/${props.post.user.avatar}?temp=${user.userUpdated}` : '/static/core/avatar.svg'
})

function likePost () {
  if (!user.success) {
    user.auth = true
    toast.$patch({message: 'Your like awaits! Sign in to show appreciation for posts.', color: 'primary', open: true})
    return
  }

  const operation = props.post.userLiked ? 'unlikeItem' : 'likeItem'

  const { mutate, onDone } = useMutation(gql`
      
      mutation ($id: ID!) { 
        ${operation} (id: $id) {
          success,
          post {
            id,
            likes,
            userLiked
          }
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

<style scoped lang="scss">
  /* Edit and delete operations */
  .edit {
    margin-right: 10px;

    &:hover {
      color: var(--ion-color-primary);
      border-color: var(--ion-color-primary);
    }
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

    &:hover {
      border-width: 2px;
      opacity: 1;
    }
  }

  .post-card {
    transition: all;
    transition-timing-function: ease-out;
    margin: 0px;

    &:hover {
      box-shadow: 0 2px 4px -1px rgba(0,0,0,.2),0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12)!important;
    }
    
    &:hover:not(:has(.operations:hover)) .like-icon {
      color: grey;
    }
  }

  ion-item {
    --min-height: 0px;
    &.image {
      --inner-padding-end: 0px;
      --padding-start: 0px;
      ion-img::part(image) {
        max-height: 600px;
        object-fit: contain;
      }
    }
    p {
      margin-bottom: 10px;
    }
  }
</style>