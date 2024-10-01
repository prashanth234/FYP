<template>
  <ion-page>
    <ion-content class="full-height" ref="content">

      <ion-refresher slot="fixed" @ionRefresh="refetch($event)">
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
            :verify="entity.details.verifyUsers"
          />

          <!-- Entity Details -->
          <ion-col 
            size="12"
            class="entity card"
          >

            <img class="image" :src="entity.details.image" alt="" />
            
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

            <ion-button
              v-else-if="entity.details.isAdmin"
              aria-label="edit.details"
              fill="outline"
              class="join-entity"
              @click="editEntityDetails(entity.details)"
              size="small"
            >
              EDIT
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
                  <a 
                    v-if="entity.details.maps"
                    :href="entity.details.maps"
                    target="_blank"
                    class="text"
                    style="text-decoration: none;"
                  >
                    {{ entity.details.city }}
                  </a>
                  <div v-else class="text">{{ entity.details.city }}</div>
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
                  v-if="entity.details.id"
                  :linkedin="entity.details.linkedin"
                  :instagram="entity.details.instagram"
                  :facebook="entity.details.facebook"
                  :whatsapp="entity.details.phone"
                  :mail="entity.details.email"
                  size="30"
                  style="padding: 0px; float: right;"
                />
              </ion-col>
      
            </ion-row>

          </ion-col>

          <!-- Admin actions -->
          <ion-col
            size="12"
          >
            <ion-row v-if="entity.details.isAdmin">

              <ion-col size="12" class="ion-no-padding" style="padding: 5px 0px;">
                <ion-accordion-group expand="inset" style="margin: 0px;">
                  <ion-accordion value="first">
                    <ion-item slot="header">
                      <ion-label>Pending Requests</ion-label>
                    </ion-item>
                    <div class="ion-padding" slot="content">
                      <JoinRequests :entityId="entity.details.id" />
                    </div>
                  </ion-accordion>
                </ion-accordion-group>
              </ion-col>

              <ion-col size="auto">
                <ion-button shape="round" fill="outline">Create Contest</ion-button>
              </ion-col>

              <ion-col size="auto">
                <ion-button shape="round" fill="outline">Create Event</ion-button>
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
            style="padding-bottom: 0px;"
            v-if="entity.details.competitions?.length"
          >
            <competitions
              @close-competition="cancelCompetition"
              @select-competition="loadCompetition"
              :vertical="false"
              :type="store.type"
            />
          </ion-col>

          <!-- Ask user to join the entity if entity is private and user not part of entity -->
          <ion-col
            size="12"
            class="ion-text-center ion-padding text-bold padding-y"
            v-if="!entity.details.ispublic && entity.details.userAccess != 'SUCCESS'"
          >
            You're not a member of this entity. Please join to view the posts.
          </ion-col>

          <ion-col
            v-else
            size="12"
            class="ion-no-padding"
          >
            <Feed
              :delete-cntrl="entity.details.isAdmin"
              :show-by-owner-tag="true"
              :type="store.type"
              :posts="posts"
              :fetchMoreCompleted="fetchMoreCompleted"
              :fetchMore="fetchMore"
              :refetch="refetch"
              :onChangeCmptType="loadCompetitionType"
            />
          </ion-col>

        </ion-row>

      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonLabel, IonAccordion, IonAccordionGroup, IonItem, IonPage, IonContent, IonRow, IonCol, IonGrid, IonIcon, IonButton, IonRefresher, IonRefresherContent, useIonRouter } from '@ionic/vue'
import { businessOutline, locationOutline, chevronDownCircleOutline } from 'ionicons/icons'
import Competitions from '@/components/CompetitionsContainer.vue'
import SocialLinks from '@/components/SocialContainer.vue'
import JoinEntity from '@/components/JoinEntityContainer.vue'
import TextClamp from 'vue3-text-clamp'
import { reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { scrollTop } from '@/composables/scroll'
import { EntityType } from '@/utils/interfaces'
import { useToastStore } from '@/stores/toast'
import { useEntityInfoStore } from '@/stores/entityInfo'
import Feed from '@/components/FeedContainer.vue'
import { feed, watchRoute } from '@/composables/feed'
import gql from 'graphql-tag'
import JoinRequests from '@/components/JoinRequestsContainer.vue'

const props = defineProps({
  id: String,
  postid: String
})

const state = reactive({
  showJoinEntity: false
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
      maps,
      phone,
      email,
      instagram,
      linkedin,
      facebook,
      userAccess,
      ispublic,
      isAdmin,
      verifyUsers,
      admins {
        id,
        username
      },
      competitions {
        id,
        name,
        description,
        lastDate,
        image,
        expired,
        points,
        message
      },
      stats {
        id,
        users,
        posts,
        categories {
          id,
          name,
          count,
          color
        }
      }
    }
  }
`

const user = useUserStore()
const auth = useAuthStore()
const toast = useToastStore()
const { content } = scrollTop()
const store = useEntityInfoStore()
const { store: entity } = watchRoute(ENTITY_DETAILS, store, props.id, props.postid)
const ionRouter = useIonRouter();

const {
  posts,
  fetchMoreCompleted,
  fetchMore,
  loadCompetitionType,
  loadCompetition,
  cancelCompetition,
  refetch
} = feed(store, content, undefined, props.id)


function openJoinEntity(ed: EntityType) {
  if (!user.success) {
    auth.showMessage('Ready to join the entity? Log in now!', 'info')
    auth.open()
    return
  }

  state.showJoinEntity = true
  return
}

function editEntityDetails(ed: EntityType) {
  store.preserve = true
  ionRouter.push(`/entity/${ed.id}`)
}

function routeTo(to: string, ed: EntityType) {
  ionRouter.push(`/${to}/${ed.id}`)
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
    border-width: 0px;
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
  // margin-top: 15px;
  margin-bottom: 5px;
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

ion-accordion.accordion-collapsing ion-item[slot='header'],
ion-accordion.accordion-collapsed ion-item[slot='header'],
ion-accordion.accordion-expanding ion-item[slot='header'],
ion-accordion.accordion-expanded ion-item[slot='header'] {
  --background: var(--ion-card-background);
}
</style>