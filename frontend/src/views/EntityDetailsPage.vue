<template>
  <ion-page>
    <ion-content>

      <ion-refresher slot="fixed" @ionRefresh="refreshPosts($event)">
        <ion-refresher-content
          :pulling-icon="chevronDownCircleOutline"
          pulling-text="Pull to refresh"
          refreshing-spinner="circles"
          refreshing-text="Refreshing..."
        >
        </ion-refresher-content>
      </ion-refresher>

      <ion-grid style="max-width: 700px;">

        <ion-row class="ion-justify-content-center" v-if="!entity.loading">

          <JoinEntity
            v-model:show="state.showJoinEntity"
            :entity="entity.details.id"
          />

          <!-- Entity Details -->
          <ion-col 
            size="12"
            class="entity card"
          >

            <img class="image" :src="entity.details.image" />

            <ion-button
              v-if="entity.details.userAccess != 'SUCCESS'"
              aria-label="join-entity.details"
              fill="outline"
              class="join-entity"
              @click="openJoinEntity(entity.details)"
              size="small"
              :disabled="entity.details.userAccess == 'PENDING'"
            >
              <span style="font-family: sans-serif;">{{ entity.details.userAccess == 'PENDING' ? 'Requested' : 'JOIN'}}</span>
            </ion-button>

            <ion-row class="details ion-padding">

              <!-- Title -->
              <ion-col size="12" class="title ion-text-start">
                {{ entity.details.name }}
              </ion-col>

              <ion-col size="12" v-if="entity.details.description">
                <text-clamp :key="entity.details.description" :text="entity.details.description" :max-lines="2" auto-resize>
                  <template #after="{ toggle, expanded, clamped }">
                    <a v-if="expanded || clamped" @click="toggle" class="cpointer">
                      {{ expanded ? ' See less' : ' See more' }}
                    </a>
                  </template>
                </text-clamp>
              </ion-col>

              <!-- Type and location -->
              <ion-col size="12">
                <div class="subtitle">
                  <ion-icon class="icon" :icon="businessOutline"></ion-icon>
                  <div class="text">{{ entity.details.type }}</div>
                </div>
                <div class="subtitle" style="padding-top: 5px">
                  <ion-icon class="icon" :icon="locationOutline"></ion-icon>
                  <div class="text">{{ entity.details.city }}</div>
                </div>
              </ion-col>

              <!-- Overall Stats -->
              <ion-col
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
                class="ion-align-self-center global-stats"
              >
                <span class="count" style="padding: 5px;">{{ entity.details.stats?.users }}</span>
                <span class="label">Users</span>
                <span class="count" style="padding: 0px 5px 0px 15px;">{{ entity.details.stats?.posts }}</span>
                <span class="label">Posts</span>
              </ion-col>

              <!-- Social Links -->
              <ion-col 
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
              >
                <social-links
                  :linkedin="entity.details.linkedin"
                  :instagram="entity.details.instagram"
                  :facebook="entity.details.facebook"
                  size="30"
                  style="padding: 0px; float: right;"
                />
              </ion-col>
      
            </ion-row>

          </ion-col>

          <!-- Entity Stats -->
          <ion-col 
            size="12"
            class="card stats"
          >

            <ion-grid class="grid">
              <ion-row class="ion-justify-content-center">
                <ion-col
                  size="8" size-xs="6" size-sm="6" size-md="3" size-lg="3" size-xl="3"
                  v-for="(stat, index) in entity.details.stats?.categories" :key="index"
                >
                  <div class="one-card" :style="`background-color: ${stat.color}`">
                    <div class="count">{{ stat.count }}</div>
                    <div class="label overflow-ellipsis" :title="stat.name">{{ stat.name }}</div>
                  </div>
                </ion-col>
              </ion-row>
            </ion-grid>
          
          </ion-col>

          <!-- Competitions -->
          <ion-col
            size="12"
            style="overflow: auto;"
            v-if="entity.details.competitions?.length"
          >
            <competitions
              type="entity"
              :vertical="false"
              @close-competition="closeCompetition"
              @select-competition="loadCompetitionPosts"
            />
          </ion-col>

          <!-- Ask user to join the entity -->
          <ion-col
            size="12"
            class="ion-text-center ion-padding text-bold padding-y"
            v-if="entity.details.userAccess != 'SUCCESS'"
          >
            You're not a member of this entity. Please join to view the posts.
          </ion-col>

          <!-- Show single post for shared posts -->
          <ion-col
            size="12"
            v-else-if="state.showSinglePost && props.postid"
          >
            <SinglePost
              :id="props.postid"
              :entity="props.id"
              @more="hidePostDetails(true)"
            />
          </ion-col>


          <!-- Entity posts -->
          <ion-col
            size="12"
            class="ion-no-padding"
            v-else-if="entityPosts?.entityPosts.posts.length"
          >

            <ion-row>

              <ion-col
                size="12"
              >
                <div class="feed">
                  <div class="title">
                    Feed
                  </div>
                  <Refresh @refresh="refreshPosts(null)" :refreshing="state.refreshing"/>
                </div>
              </ion-col>

              <ion-col
                size="12"
                v-if="entityPosts.entityPosts.posts.length"
                v-for="post in entityPosts.entityPosts.posts"
                :key="post.id"
              >
                <post :post="post"></post>
              </ion-col>

            </ion-row>

            <ion-infinite-scroll 
              :disabled="state.showSinglePost || fetchMoreCompleted"
              :key="`${fetchMoreCompleted}`"
              @ionInfinite="fetchMore"
              :threshold="user.success ? '400px' : '30px'"
            >
              <ion-infinite-scroll-content loading-text="Loading..." loading-spinner="bubbles"></ion-infinite-scroll-content>
            </ion-infinite-scroll>

          </ion-col>

          <!-- No posts message -->
          <ion-col
            size="12"
            class="ion-text-center text-bold padding-y"
            v-else
          >
            Dive in and share your creative posts! You can be the first to post.
          </ion-col>

        </ion-row>

      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonRow, IonCol, IonGrid, IonIcon, IonButton, IonInfiniteScroll, IonInfiniteScrollContent, InfiniteScrollCustomEvent, IonRefresher, IonRefresherContent, RefresherCustomEvent} from '@ionic/vue'
import { businessOutline, locationOutline, chevronDownCircleOutline } from 'ionicons/icons'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import Competitions from '@/components/CompetitionsContainer.vue'
import SocialLinks from '@/components/SocialContainer.vue'
import JoinEntity from '@/components/JoinEntityContainer.vue'
import SinglePost from '@/components/SinglePostContainer.vue'
import Refresh from '@/components/RefreshContainer.vue'
import { getPosts } from '@/composables/posts'
import Post from '@/components/PostContainer.vue'
import TextClamp from 'vue3-text-clamp'
import { reactive, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { scrollTop } from '@/composables/scroll'
import { EntityType } from '@/utils/interfaces'
import { useToastStore } from '@/stores/toast'
import { useJoinEntityAPI } from '@/composables/entity'
import { useEntityInfoStore } from '@/stores/entityInfo'
import { CompetitionInfo } from '@/utils/interfaces';


const user = useUserStore()
const auth = useAuthStore()
const toast = useToastStore()
const { content } = scrollTop()
const entity  = useEntityInfoStore()
const route = useRoute()


const props = defineProps({
  id: String,
  postid: String
})

const state = reactive({
  showJoinEntity: false,
  showSinglePost: !!props.postid,
  refreshing: false
})

props.id && entity.getEntityDetails(props.id)

// When another entity is opened after a entity is opened, page is not rendered again so need to watch router params
watch(() => route.params.id, () => {
  if (route.name == 'entityDetails' && route.params.id == props.id) {
    entity.getEntityDetails(props.id)
  }
})

// When the router leaves the details page, clear the entity information store
onBeforeRouteLeave(() => {
  entity.details.name && entity.$reset()
  props.postid && hidePostDetails(false)
})

const { 
  posts: entityPosts,
  loading: loadingPosts,
  getMore,
  fetchMoreCompleted,
  refetch,
  variables
} = getPosts('entityPosts', undefined, undefined, props.id)

function loadCompetitionPosts(competition: CompetitionInfo) {
  hidePostDetails(true)
  variables.competition.value = competition.id
}

function closeCompetition() {
  if (!variables.competition.value) { return }
  variables.competition.value = undefined
}

function hidePostDetails(value: boolean) {
  state.showSinglePost = !value
}

function openJoinEntity(ed: EntityType) {
  if (!user.success) {
    auth.showMessage('Ready to join the entity? Log in now!', 'info')
    auth.open()
    return
  }

  if (ed.ispublic) {
    // For public entity directly add user to entity
    const { mutate, onDone, onError } = useJoinEntityAPI()
    mutate({entityId: ed.id})
    onDone(({data}) => {
      toast.$patch({message: data.joinEntity.message, color: 'success', open: true})
    })
  } else {
    // For private entity ask for code or proof
    state.showJoinEntity = true
  }
}

function fetchMore(ev: InfiniteScrollCustomEvent) {
  getMore(ev, content)
}

async function refreshPosts(event: RefresherCustomEvent | null) {
  state.refreshing = true
  await refetch()
  state.refreshing = false
  event?.target && event.target.complete && event.target.complete()
}

</script>

<style lang="scss" scoped>

.entity {
  position: relative;
  margin-top: 90px;
  max-width: 750px !important;

  .image {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius:  50%;
    position: absolute;
    left: 20px;
    top: -80px;
  }

  .details {
    padding-top: 65px;
  }

  .title {
    font-size: 24px;
    font-weight: 590;
    color: var(--ion-color-dark);
    letter-spacing: 0.4px;
  }

  .subtitle {
    color: var(--ion-color-medium-shade);
    display: flex;
    margin-top: 5px;

    .icon {
      font-size: 21px;
    }
    
    .text {
      font-size: 17px;
      padding-left: 7px;
      padding-right: 7px;
    }
  }

}

.global-stats {
  font-size: 17px;

  .count {
    font-weight: 590;
  }

  .label {
    font-weight: 450;
  }
}

.stats {
  margin-top: 20px;
  color: black;
  max-width: 750px !important;

  .grid {
    --ion-grid-column-padding: 7px;
    --ion-grid-padding: 0px;
  }

  .one-card {
    padding: 15px;
    border-radius: 10px;
  }

  .label {
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.5px;
    line-height: 3;
  }

  .count {
    font-size: 24px;
    font-weight: 590;
  }
}

.join-entity {
  margin: 10px;
  position: absolute;
  right: 0;
}

@media only screen and (max-width: 576px) {
	// For small screens
  .entity {

    .details {
      padding-top: 55px;
    }

    .image {
      width: 130px;
      height: 130px;
    }

    .title {
      font-size: 22px;
    }

    .subtitle {
      
      .text {
        font-size: 17px;
      }

      .icon {
        font-size: 21px;
      }

    }
  }
}

.padding-y {
  padding-top: 25px;
  padding-bottom: 25px;
}
</style>