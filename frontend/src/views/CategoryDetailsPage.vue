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

      <ion-grid>

        <ion-row>

          <!-- Category details and posts -->
          <ion-col size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8"
            class="posts" :class="{'post-col': posts.total > 5}"
          >

            <ion-row class="ion-justify-content-center">

              <!-- Category Details -->
              <ion-col size-xs="12" size-sm="12" size-md="11"
                style="max-width: 800px;" class="ion-no-padding"
              >

                <ion-row>

                  <!-- Information about category -->
                  <ion-col size="12">

                    <ion-card style="min-height: 100px;" class="ion-padding border-radius-std ion-no-margin" >

                        <div class="title category">
                          {{ category.details.name }}
                        </div>

                        <div class="description category">
                          {{ category.details.description }}
                        </div>
                        
                    </ion-card>

                  </ion-col>

                  <!-- Competitions for small screens -->
                  <ion-col size="12"
                    class="ion-hide-md-up" style="padding-bottom: 0px;"
                  >
                    <competitions
                      @close-competition="cancelCompetition"
                      @select-competition="loadCompetition"
                      :vertical="false"
                      type="category"
                    />
                  </ion-col>

                  <!-- Feed -->
                  <ion-col size="12" class="ion-no-padding">
                    
                    <Feed
                      type="catgory"
                      :posts="posts"
                      :fetchMoreCompleted="fetchMoreCompleted"
                      :fetchMore="fetchMore"
                      :refetch="refetch"
                      :onChangeCmptType="loadCompetitionType"
                    />
                    
                  </ion-col>

                </ion-row>
                
              </ion-col>

            </ion-row>

          </ion-col>

          <!-- Competitions for large screens -->
          <ion-col size="4" size-xs="12" size-sm="12" size-md="4" size-lg="4" size-xl="4"
            class="ion-hide-md-down"
          >
            <competitions
              @select-competition="loadCompetition"
              @close-competition="cancelCompetition"
              :vertical="true"
              type="category"
            />
          </ion-col>

        </ion-row>

      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonRefresher, IonRefresherContent, IonPage, IonCard, IonContent, IonCol, IonGrid, IonRow } from '@ionic/vue'
import Competitions from '@/components/CompetitionsContainer.vue'
import Feed from '@/components/FeedContainer.vue'
import { feed, watchRoute } from '@/composables/feed'
import { scrollTop } from '@/composables/scroll'
import { chevronDownCircleOutline } from 'ionicons/icons'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import gql from 'graphql-tag'

const props = defineProps({
  id: String,
  postid: String
})

const CATEGORY_DETAILS = gql`
  query categoryDetails ($id: ID!) {
    categoryDetails (id: $id) {
      id,
      name,
      description,
      oftype,
      competitions {
          id,
          name,
          description,
          lastDate,
          image,
          expired,
          points,
          message
      }
    }
  }
`

const { content } = scrollTop()
const store = useCategoryInfoStore()
const { store: category } = watchRoute(CATEGORY_DETAILS, store, props.id, props.postid)

const {
  posts,
  fetchMoreCompleted,
  fetchMore,
  loadCompetitionType,
  loadCompetition,
  cancelCompetition,
  refetch
} = feed(store, content, props.id)

</script>

<style scoped lang="scss">
.posts {
  padding: 2px;
  ion-card {
    margin-left: 0px;
    margin-right: 0px;
  }
}
ion-content::part(scroll) {
  padding-top: 0px;
}
ion-grid {
  --ion-grid-padding: 0px;
  --ion-grid-column-padding: 8px;
}
.post-col {
  min-height: 100vh;
}
.category {
  &.title {
    color: var(--ion-color-dark);
    font-size: 19px;
    font-weight: 580;
    text-transform: uppercase;
    line-height: 1.8;
  }
  &.description {
    color: var(--ion-color-dark-tint);
  }
}
.competition {
  border-left: 4px solid var(--ion-color-light-shade);
  padding-left: 7px;
  margin-top: 20px;

  .title {
    color: var(--ion-color-dark);
    font-size: 17px;
    font-weight: 580;
    line-height: 1.6;
  }
  .description {
    color: var(--ion-color-dark-tint);
  }
}

@media only screen and (max-width: 576px) {
	// For small screens
  .category {
    &.title {
      font-size: 19px;
    }
  }
}
</style>