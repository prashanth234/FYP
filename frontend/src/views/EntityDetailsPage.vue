<template>
  <ion-page>
    <ion-content>

      <ion-grid>

        <ion-row class="ion-justify-content-center">

          <!-- Entity Details -->
          <ion-col 
            size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8"
            class="entity card"
          >

            <img class="image" :src="`/media/categories/ART.jpg`" />

            <ion-row class="details ion-padding">

              <!-- Title -->
              <ion-col size="12" class="title ion-text-start">
                Test College of Engineering
              </ion-col>

              <ion-col size="12">
                <!-- <text-clamp :key="post.description" :text="post.description" :max-lines="2" auto-resize>
                  <template #after="{ toggle, expanded, clamped }">
                    <a v-if="expanded || clamped" @click="toggle" class="cpointer">
                      {{ expanded ? ' See less' : ' See more' }}
                    </a>
                  </template>
                </text-clamp> -->
                Selfdive is your go-to platform for sharing drawings, stories, crafts, photographs, and more. Earn rewards by showcasing your work in contests
              </ion-col>

              <!-- Type and location -->
              <ion-col size="12">
                <div class="subtitle">
                  <ion-icon class="icon" :icon="businessOutline"></ion-icon>
                  <div class="text">School</div>
                </div>
                <div class="subtitle" style="padding-top: 5px">
                  <ion-icon class="icon" :icon="locationOutline"></ion-icon>
                  <div class="text">Hyderabad</div>
                </div>
              </ion-col>

              <!-- Overall Stats -->
              <ion-col
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
                class="ion-align-self-center global-stats"
              >
                <span class="count" style="padding: 5px;">250</span>
                <span class="label">Users</span>
                <span class="count" style="padding: 0px 5px 0px 15px;">250</span>
                <span class="label">Posts</span>
              </ion-col>

              <!-- Social Links -->
              <ion-col 
                size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6"
              >
                <social-links
                  linkedin="teswtin"
                  instagram="tsting"
                  facebook="facebook"
                  size="30"
                  style="padding: 0px; float: right;"
                />
              </ion-col>
      
            </ion-row>

          </ion-col>

          <!-- Entity Stats -->
          <ion-col 
            size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8"
            class="card stats"
          >

            <ion-grid class="grid">
              <ion-row class="ion-justify-content-center">
                <ion-col
                  size="8" size-xs="6" size-sm="6" size-md="3" size-lg="3" size-xl="3"
                  v-for="(stat, index) in stats" :key="index"
                >
                  <div class="one-card" :style="`background-color: ${stat.color}`">
                    <div class="count">{{ stat.count }}</div>
                    <div class="label overflow-ellipsis" :title="stat.label">{{ stat.label }}</div>
                  </div>
                </ion-col>
              </ion-row>
            </ion-grid>
          
          </ion-col>

          <ion-col
            size="12"
            v-for="post in entity?.entityPosts?.posts"
            :key="post.id"
          >
            <post :post="post"></post>
          </ion-col>

        </ion-row>

      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonRow, IonCol, IonGrid, IonIcon  } from '@ionic/vue'
import { businessOutline, locationOutline } from 'ionicons/icons'
import SocialLinks from '@/components/SocialContainer.vue'
import Post from '@/components/PostContainer.vue'
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { reactive } from 'vue'
import TextClamp from 'vue3-text-clamp'

const props = defineProps({
  id: String
})

const stats = reactive([
  {
    label: 'Art',
    color: '#E8FAE5',
    count: 300
  },
  {
    label: 'Photography',
    color: '#FDF0EB',
    count: 250
  },
  {
    label: 'Stories',
    color: '#E8F8FC',
    count: 200
  },
  {
    label: 'Crafts',
    color: '#E5EBFF',
    count: 100
  }
])

const ENTITY_POSTS_QUERY = gql`
  query EntityPosts ($id: ID!) {
    entityPosts (id: $id) {
      posts {
        id,
        likes,
        userLiked,
        description,
        createdAt,
        isBot,
        postfileSet {
          file,
          width,
          height
        },
        user {
          id,
          username,
          avatar
        },
        category {
          oftype
        }
      },
      total
    }
  }
`

const { result: entity, loading } = useQuery(ENTITY_POSTS_QUERY, () => ({
  id: props.id,
}))
</script>

<style lang="scss" scoped>

.card {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 2px;
  border-radius: 10px;
  background-color: var(--ion-card-background);
}

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
      font-size: 22px;
    }
    
    .text {
      font-size: 18px;
      padding-left: 7px;
      padding-right: 7px;
    }
  }

}

.global-stats {
  font-size: 18px;

  .count {
    font-weight: 590;
  }

  .label {
    font-weight: 450;
  }
}

.stats {
  margin: 20px 0;
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