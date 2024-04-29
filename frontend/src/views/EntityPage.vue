<template>
  <ion-page>
    <ion-content>

      <!-- Search Bar -->
      <ion-row class="ion-justify-content-center ion-padding-vertical">
        <ion-col size-xs="12" size-sm="12" size-md="8" size-lg="6" size-xl="6">
          <ion-searchbar class="search" placeholder="Search Entity" v-model="state.search"></ion-searchbar>
        </ion-col>
      </ion-row>

      <ion-row>
        <ion-col
          size="3"
          v-for="entity in entities" :key="entity.id"
        >
          <ion-card class="card hover cpointer" @click="openEntity(entity)">

            <div class="content">

              <ion-row class="ion-nowrap">

                <ion-col class="ion-align-self-end"size="auto">
                  <img class="image" :src="`/media/categories/ART.jpg`" />
                </ion-col>

                <ion-col class="ion-padding-start">
                  <div class="title ion-color-dark">{{ entity.name }}</div>
                  <ion-grid class="subtitle">
                    <ion-row>
                      <ion-col size="auto" style="padding-right: 4px;">
                        <ion-icon class="icon" :icon="businessOutline"></ion-icon>
                      </ion-col>
                      <ion-col class="text">School</ion-col>
                    </ion-row>
                    <ion-row>
                      <ion-col size="auto" style="padding-right: 4px;">
                        <ion-icon class="icon" :icon="locationOutline"></ion-icon>
                      </ion-col>
                      <ion-col class="text">Hyderabad</ion-col>
                    </ion-row>
                  </ion-grid>
                </ion-col>

              </ion-row>

              <ion-row style="border-bottom: 1px solid var(--ion-color-secondary-tint); margin: 10px 5px;"></ion-row>

              <ion-row class="ion-text-center stat">

                <ion-col size="6">

                  <div>Users</div>
                  <div>250</div>

                </ion-col>

                <ion-col size="6">

                  <div>Posts</div>
                  <div>250</div>

                </ion-col>

              </ion-row>

            </div>

          </ion-card>
        </ion-col>
        
        <ion-col size="12" v-if="!loading && !entities.length" class="ion-text-center ion-padding">
          Couldn't find your entity please register
        </ion-col>

      </ion-row>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonGrid, IonPage, IonContent, IonSearchbar, useIonRouter, IonIcon, IonRow, IonCol, IonCardTitle, IonCardHeader, IonCard, IonCardSubtitle  } from '@ionic/vue'
import { businessOutline, locationOutline } from 'ionicons/icons'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { EntityType } from '@/utils/interfaces';
import { reactive, computed } from 'vue';

const ionRouter = useIonRouter();
const state = reactive({
  search: ''
})

const { result: data, loading } : { result: any, loading: any } = useQuery(gql`
                                        query Entities {
                                          entities {
                                            id,
                                            name,
                                            description
                                          }
                                        }
                                      `)

const entities = computed(() => {
  if (data.value?.entities) {
    if (state.search) {
      return data.value.entities.filter((entity: EntityType) => entity.name.toLowerCase().includes(state.search.toLowerCase()))
    } else {
      return data.value.entities
    }
  }
  return []
})


function openEntity (entity: EntityType) {
  ionRouter.push(`entity/${entity.id}`)
}
</script>

<style lang="scss" scoped>
.search {
  --border-radius: 10px
}
.card {
  border-radius: 7px;
  border: 1px solid var(--ion-color-secondary-tint);
  .content {
    padding: 7px;
  }
  .title {
    font-size: 20px;
    font-weight: 600;
    color: var(--ion-color-dark);
  }
  .subtitle {
    line-height: 1.5;
    .icon {
      font-size: 20px;
    }
  }
  .image {
    border: 1px solid var(--ion-color-secondary-tint);
    border-radius: 4px;
    object-fit: cover;
    width: 60px;
    height: 60px;
  }
  .stat {
    // background-color: #e8f1ff;
    line-height: 1.8;
    margin: 5px;
    font-size: 14px;
    font-weight: 600;
    // color: var(--ion-card-color);
    border-radius: 5px;
  }
}
.subtitle {
  --ion-grid-padding: 0px;
  --ion-grid-column-padding:  0px;
  padding-top: 5px;
  .icon {
    font-size: 18px;
  }
  .text {
    font-size: 14px;
  }
}

</style>