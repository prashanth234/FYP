<template>
  <ion-card class="border-radius-std post-card">

    <ion-card-content @dblclick="likePost()" class="ion-no-padding">
      <ion-list class="ion-no-padding">

        <ion-item lines="none" class="line" style="padding: 8px 0px;">

          <ion-avatar slot="start" style="margin: 0px 10px 0px 0px">
            <img
              alt="avatar"
              :src="userAvatar"
            />
          </ion-avatar>

          <div style="flex: 1">
            {{ post.user.username }}
            <div
              v-if="props.showByOwnerTag && post.byEntityAdmin"
              class="post-subtitle"
            >
              Post by Owner
            </div>
            <div
              v-else-if="props.showFromEntityTag && post.entity"
              class="post-subtitle one-line-ellipsis"
            >
              {{ `From ${post.entity.name} Entity` }}
            </div>
          </div>

          <ion-icon
            v-if="props.showEdit && (!post.competition || !post.competition.expired)"
            @click.stop="emit('editPost')"
            class="cpointer edit operations"
            :icon="pencilOutline"
          />

          <ion-icon 
            v-if="props.showDelete && (!post.competition || !post.competition.expired)"
            @click.stop="emit('deletePost')"
            class="cpointer delete operations"
            :icon="trashOutline"
          />

          <div v-if="props.position">
            <strong>#{{props.position}}</strong>
          </div>

          <ion-badge v-else-if="post.isBot" color="primary" slot="end" style="margin-right: -5px; font-size: 12px; font-weight: 550;">Sample</ion-badge>

        </ion-item>

        <ion-item
          class="image"
          lines="none"
          style="padding-top: 12px;"
          v-if="post.postfileSet.length"
          :class="{'content-padding': !post.description}"
        >
        
          <picture class="ml-auto mr-auto">
            <source :srcset="post.postfileSet[0].files.lg" media="(min-width: 600px)" />
            <source :srcset="post.postfileSet[0].files.md" media="(max-width: 600px)" />
            <img
              :src="post.postfileSet[0].files.og"
              :alt="post.description"
              :width="post.postfileSet[0].width"
              :height="post.postfileSet[0].height"
              loading="eager"
              fetchpriority="high"
            />
          </picture>

        </ion-item>

        <ion-item
          v-if="post.description"
          lines="none"
          class="post-description content-padding"
        >
          <text-clamp :key="post.description" :text="post.description" :max-lines="post?.category.oftype == 'TEXT' ? 10 : 3" auto-resize>
            <template #after="{ toggle, expanded, clamped }">
              <a v-if="expanded || clamped" @click="toggle" class="cpointer">
                {{ expanded ? ' See less' : ' See more' }}
              </a>
            </template>
          </text-clamp>
        </ion-item>

        <ion-item lines="none" class="line-top" style="padding: 8px 0px 8px 5px;">

          <transition name="slide-up" mode="out-in">
            <div v-if="post.userLiked" style="height: 28px;">
              <Clapped
                @click="likePost()"
                width="28px"
                height="28px"
                class="cpointer"
              ></Clapped>
            </div>
            <div v-else style="height: 28px;">
              <ClapOutline
                @click="likePost()"
                width="28px"
                height="28px"
                class="like-icon cpointer"
              ></ClapOutline>
            </div>
          </transition>

          <ion-label
            v-if="!post.isBot"
            class="like-count-label"
          > 
            <span>{{ post.likes < 0 ? 0 : post.likes }}</span>
          </ion-label>

          <ion-modal
            class="share-modal"
            :is-open="share.show"
            :show-backdrop="true"
            @willDismiss="closeSharePost"
          >
            <div 
              class="ion-padding ion-margin ion-text-center"
            >
              <div
                lines="none"
                style="font-size: 18px; font-weight: 550; margin-bottom: 15px;"
              >
                Share your post to help it reach more people!
              </div>
              <ion-card class="ion-margin-bottom ion-padding" style="color: var(--ion-color-dark-tint)">
                {{share.url}}
              </ion-card>
              <ShareNetwork
                v-for="network in share.networks"
                :network="network.network"
                :key="network.network"
                :url="share.url"
                :title="share.title"
                :description="share.description"
                :quote="share.quote"
                :hashtags="share.hashtags"
                class="ion-padding"
                @open="closeSharePost"
              >
                <ion-icon :style="`color: ${network.color}; font-size: 40px`" :icon="network.icon"></ion-icon>
              </ShareNetwork>
              <div class="ion-margin-top">
                <ion-button @click="closeSharePost" size="small" color="light">Close</ion-button>
              </div>
            </div>
          </ion-modal>
          
          <ion-icon
            v-if="!post.isBot"
            @click="sharePost()"
            class="cpointer share-icon"
            style="float: right;"
            :icon="shareSocialOutline"
          />
        </ion-item>

        <slot name="bottom"></slot>

      </ion-list>
    </ion-card-content>

  </ion-card>
</template>

<script lang="ts" setup>
import { IonButton, IonModal, IonList, IonItem, IonImg, IonLabel, IonAvatar, IonCard, IonCardContent, IonIcon, IonBadge  } from '@ionic/vue';
import { pencilOutline, trashOutline, shareSocialOutline, logoWhatsapp, logoFacebook, logoLinkedin } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { computed, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import TextClamp from 'vue3-text-clamp'
import ClapOutline from './icons/clapOutline.vue'
import Clapped from './icons/clapped.vue'
import { useAuthStore } from '@/stores/auth';

const user = useUserStore()
const auth = useAuthStore()
const props = defineProps([
  'post',
  'showEdit',
  'showDelete',
  'position',
  'showByOwnerTag',
  'showFromEntityTag'
])

const share = reactive({
  url: '',
  title: 'Share in the Joy!',
  description: "Hey there, I’ve just posted about something I absolutely love, and I'm excited to have you all join in. Please take a moment to check it out and hit that like button.",
  quote: '',
  hashtags: '',
  networks: [
    { network: 'whatsapp', name: 'Whatsapp', icon: logoWhatsapp, color: '#25d366' },
    { network: 'facebook', name: 'Facebook', icon: logoFacebook, color: '#1877f2' },
    { network: 'linkedin', name: 'LinkedIn', icon: logoLinkedin, color: '#007bb5' }
  ],
  show: false
})

share.url = document.URL.replace(/posts.*/, `posts/${props.post.id}`)

const emit = defineEmits<{
  (e: 'editPost'): void
  (e: 'deletePost'): void
}>()

const userAvatar = computed(() => {
  return props.post.user.avatar || '/static/core/avatar.svg'
})

function sharePost() {
  share.show = true
}

function closeSharePost() {
  share.show = false
}

function likePost() {
  if (!user.success) {
    auth.showMessage('Your like awaits! Sign in to show appreciation for posts.', 'info')
    auth.open()
    return
  }

  // const operation = props.post.userLiked ? 'unlikeItem' : 'likeItem'

  const { mutate, onDone } = useMutation(gql`
      
      mutation ($id: ID!) { 
        likeItem (id: $id) {
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
    // transition: all;
    // transition-timing-function: ease-out;

    // &:hover {
      // box-shadow: 0 2px 4px -1px rgba(0,0,0,.2),0 4px 5px 0 rgba(0,0,0,.14),0 1px 10px 0 rgba(0,0,0,.12)!important;
      // box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
    // }
    
    // &:hover:not(:has(.operations:hover)) .like-icon {
      // opacity: 0.8;
    // }
  }

  @media only screen and (max-width: 576px) {
    .image img {
      min-height: 150px !important;
    }
  }

  ion-item {
    --min-height: 0px;
    &.image {
      --inner-padding-end: 0px;
      --padding-start: 0px;
      img {
        max-height: 500px;
        min-height: 250px;
        object-fit: contain;
        max-inline-size: 100%;
        block-size: auto;
      }
      &::part(native) .input-wrapper {
        justify-content: center;
      }
    }
    // &.image::part(native) {
      // background-color: whitesmoke;
      // filter: blur(1px);
    // }
    p {
      margin-bottom: 10px;
    }
  }
  .content-padding {
    padding-top: 12px;
    padding-bottom: 12px;
  }
  .post-description {
    font-size: 15px;
    white-space: pre-wrap;
    a:hover {
      text-decoration: underline;
    }
  }
  .like-count-label {
    font-weight: 500;
    font-size: 14px;
    padding-left: 10px;
    margin: 0px;
  }
  .like-icon {
    opacity: 0.6;
  }
  .share-icon {
    opacity: 0.5;
    &:hover {
      opacity: 1;
    }
  }
  .share-modal {
    --max-width: 90%;
    --height: auto;
  }
  @media only screen and (min-width: 576px) {
    .share-modal {
      --max-width: 470px;
    }
  }
  .slide-up-enter-active,
  .slide-up-leave-active {
    transition: all 0.25s ease-out;
  }

  .slide-up-enter-from {
    opacity: 0;
    transform: translateY(30px);
  }

  .slide-up-leave-to {
    opacity: 0;
    transform: translateY(-30px);
  }
  
  .post-subtitle {
    font-size: 14px;
    color: grey;
  }
</style>