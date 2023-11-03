<template>
  <ion-card class="border-radius-std post-card" color="light">

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
            v-if="props.showEdit && (!post.competition || !post.competition.expired)"
            @click.stop="emit('editPost')"
            class="cpointer edit operations"
            :icon="pencilOutline"
          />
          <ion-icon 
            v-if="props.showEdit && (!post.competition || !post.competition.expired)"
            @click.stop="emit('deletePost')"
            class="cpointer delete operations"
            :icon="trashOutline"
          />
          <div v-if="props.position">
            <strong>#{{props.position}}</strong>
          </div>
          <ion-badge v-else-if="post.isBot" color="primary" slot="end" style="margin-right: -5px; font-size: 12px; font-weight: 550;">Sample</ion-badge>
        </ion-item>

        <ion-item class="image" lines="none" style="padding-top: 12px;" v-if="post.postfileSet.length">
          <ion-img 
            class="ml-auto mr-auto"
            :src="`/media/${post.postfileSet[0].file}`"
            alt="Image"
          />
        </ion-item>

        <ion-item v-if="post.description" lines="none" class="post-description">
          <text-clamp :text="post.description" :max-lines='3' auto-resize>
            <template #after="{ toggle, expanded, clamped }">
              <a v-if="expanded || clamped" @click="toggle" class="cpointer">
                {{ expanded ? ' See less' : ' See more' }}
              </a>
            </template>
          </text-clamp>
        </ion-item>

        <ion-item lines="none" class="line-top" style="padding: 3px 0px;">
          <ion-icon
            @click="likePost()"
            class="cpointer"
            v-if="post.userLiked"
            style="color:rgb(246, 73, 73)"
            :icon="heart"
            size="large"
          />
          <ion-icon
            @click="likePost()"
            class="like-icon cpointer"
            v-else
            :icon="heartOutline"
            size="large"
          />
          <ion-label
            class="ion-padding-start"
          >
            <span v-if="post.isBot">Like</span>
            <span v-else>{{ post.likes < 0 ? 0 : post.likes }} Like{{post.likes == 1 ? '' : 's'}}</span>
          </ion-label>
        </ion-item>

        <slot name="bottom"></slot>

      </ion-list>
    </ion-card-content>

  </ion-card>
</template>

<script lang="ts" setup>
import { IonList, IonItem, IonImg, IonLabel, IonAvatar, IonCard, IonCardContent, IonIcon, IonBadge, useIonRouter  } from '@ionic/vue';
import { heartOutline, heart, pencilOutline, trashOutline, expand } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import TextClamp from 'vue3-text-clamp'

const user = useUserStore()
const props = defineProps(['post', 'showEdit', 'position'])

const emit = defineEmits<{
  (e: 'editPost'): void
  (e: 'deletePost'): void
}>()

const userAvatar = computed(() => {
  return props.post.user.avatar ? `/media/${props.post.user.avatar}` : '/static/core/avatar.svg'
})

function likePost () {
  if (!user.success) {
    user.authMessage = 'Your like awaits! Sign in to show appreciation for posts.'
    user.auth = true
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
    max-width: 480px;
    margin: auto !important;
    transition: all;
    transition-timing-function: ease-out;

    &:hover {
      // box-shadow: 0 2px 4px -1px rgba(0,0,0,.2),0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12)!important;
      // box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
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
        max-height: 500px;
        min-height: 250px;
        object-fit: contain;
      }
    }
    &.image::part(native) {
      // background-color: whitesmoke;
      // filter: blur(1px);
    }
    p {
      margin-bottom: 10px;
    }
  }
  .post-description {
    padding-top: 12px;
    padding-bottom: 12px;
    font-size: 14px;
    a:hover {
      text-decoration: underline;
    }
  }
</style>