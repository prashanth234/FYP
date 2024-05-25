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

        <ion-row class="ion-justify-content-center" v-if="!loadingDetails">

          <JoinEntity
            v-model:show="state.showJoinEntity"
            :entity="ed.entityDetails.id"
          />

          <!-- Entity Details -->
          <ion-col 
            size="12"
            class="entity card"
          >

            <img class="image" :src="ed.entityDetails.image" />

            <ion-button
              v-if="ed.entityDetails.userAccess != 'SUCCESS'"
              aria-label="join-entity"
              fill="outline"
              class="join-entity"
              @click="openJoinEntity"
              size="small"
              :disabled="ed.entityDetails.userAccess == 'PENDING'"
            >
              {{ ed.entityDetails.userAccess == 'PENDING' ? 'Requested' : 'JOIN'}}
            </ion-button>

            <ion-row class="details ion-padding">

              <!-- Title -->
              <ion-col size="12" class="title ion-text-start">
                {{ ed.entityDetails.name }}
              </ion-col>

              <ion-col size="12" v-if="ed.entityDetails.description">
                <text-clamp :key="ed.entityDetails.description" :text="ed.entityDetails.description" :max-lines="2" auto-resize>
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
                  <div class="text">{{ ed.entityDetails.type }}</div>
                </div>
                <div class="subtitle" style="padding-top: 5px">
                  <ion-icon class="icon" :icon="locationOutline"></ion-icon>
                  <div class="text">{{ ed.entityDetails.city }}</div>
                </div>
              </ion-col>

              <!-- Overall Stats -->
              <ion-col
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
                class="ion-align-self-center global-stats"
              >
                <span class="count" style="padding: 5px;">{{ ed.entityDetails.allStats.users }}</span>
                <span class="label">Users</span>
                <span class="count" style="padding: 0px 5px 0px 15px;">{{ ed.entityDetails.allStats.posts }}</span>
                <span class="label">Posts</span>
              </ion-col>

              <!-- Social Links -->
              <ion-col 
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
              >
                <social-links
                  :linkedin="ed.entityDetails.linkedin"
                  :instagram="ed.entityDetails.instagram"
                  :facebook="ed.entityDetails.facebook"
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
                  v-for="(stat, index) in ed.entityDetails.allStats.categories" :key="index"
                >
                  <div class="one-card" :style="`background-color: ${stat.color}`">
                    <div class="count">{{ stat.count }}</div>
                    <div class="label overflow-ellipsis" :title="stat.name">{{ stat.name }}</div>
                  </div>
                </ion-col>
              </ion-row>
            </ion-grid>
          
          </ion-col>

          <!-- Private Entity Message-->
          <ion-col
            size="12"
            class="ion-text-center ion-padding text-bold"
            v-if="!ed.entityDetails.ispublic && ed.entityDetails.userAccess != 'SUCCESS'"
          >
            This entity is private. Only members have access to posts.
          </ion-col>

          <!-- Show single post for shared posts -->
          <ion-col
            size="12"
            v-else-if="state.showSinglePost && props.postid"
          >
            <SinglePost
              :id="props.postid"
              :entity="props.id"
              @more="state.showSinglePost = false"
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

              <ion-col
                size="12"
                class="ion-text-center ion-padding text-bold"
                v-else
              >
                No posts here yet! Join in and start sharing!
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

        </ion-row>

      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonRow, IonCol, IonGrid, IonIcon, IonButton, IonInfiniteScroll, IonInfiniteScrollContent, InfiniteScrollCustomEvent, IonRefresher, IonRefresherContent, RefresherCustomEvent} from '@ionic/vue'
import { businessOutline, locationOutline, chevronDownCircleOutline } from 'ionicons/icons'
import SocialLinks from '@/components/SocialContainer.vue'
import JoinEntity from '@/components/JoinEntityContainer.vue'
import SinglePost from '@/components/SinglePostContainer.vue'
import Refresh from '@/components/RefreshContainer.vue'
import { getPosts } from '@/composables/posts'
import Post from '@/components/PostContainer.vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import TextClamp from 'vue3-text-clamp'
import { useMainStore } from '@/stores/main'
import { reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { scrollTop } from '@/composables/scroll'


const user = useUserStore()
const auth = useAuthStore()
const main = useMainStore()
const { content } = scrollTop()


const props = defineProps({
  id: String,
  postid: String
})

const state = reactive({
  showJoinEntity: false,
  showSinglePost: !!props.postid,
  refreshing: false
})

const ENTITY_DETAILS = gql`
  query EntityDetails ($id: ID!) {
    entityDetails (id: $id) {
      id,
      name,
      description,
      type,
      image,
      city,
      instagram,
      linkedin,
      facebook,
      userAccess,
      allStats {
        users,
        posts,
        categories {
          name,
          count,
          color
        }
      }
    }
  }
`

const { result: ed, loading: loadingDetails, onResult } = useQuery(ENTITY_DETAILS, () => ({
  id: props.id,
}))

onResult(({loading}) => {
  main.pageloading = loading
})

const { 
  posts: entityPosts,
  loading: loadingPosts,
  getMore,
  fetchMoreCompleted,
  refetch
} = getPosts('entityPosts', undefined, undefined, props.id)

function openJoinEntity() {
  if (!user.success) {
    auth.showMessage('Ready to join the entity? Log in now!', 'info')
    auth.open()
    return
  }
  state.showJoinEntity = true
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
</style>