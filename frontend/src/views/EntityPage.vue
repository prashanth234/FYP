<template>
  <ion-page>
    <ion-content>

      <!-- Search Bar -->
      <ion-row class="ion-justify-content-center ion-padding-vertical">
        <ion-col size-xs="12" size-sm="12" size-md="8" size-lg="6" size-xl="6">
          <ion-searchbar class="search" placeholder="Search Entity" v-model="state.search"></ion-searchbar>
        </ion-col>
        <ion-col size="12" class="ion-text-center grey-text" style="padding: 5px;">
          Don't see your entity? Be the one to represent your entity by clicking <a @click="createEntity" class="cpointer text-bold">request entity</a>
        </ion-col>
      </ion-row>

      <div class="grid-container">
        <div
          class="grid-item cpointer hover"
          v-for="entity in entities" :key="entity.id"
          @click="openEntity(entity)"
        >
          <ion-card class="card" >

            <div class="content">

              <ion-row class="ion-nowrap" style="padding: 12px">

                <ion-col class="ion-align-self-end" size="auto">
                  <img class="image" :src="entity.image" />
                </ion-col>

                <ion-col style="padding-left: 10px;" class="overflow-ellipsis">
                  <div>{{ entity.type }}</div>
                  <div class="title ion-color-dark overflow-ellipsis" :title="entity.name" >{{ entity.name }}</div>
                </ion-col>

              </ion-row>

              <ion-row class="line"></ion-row>

              <ion-row class="ion-text-center" style="padding: 5px">

                <ion-col size="6">

                  <div class="stat">
                    <ion-icon class="icon" :icon="personOutline"></ion-icon>
                    <div class="text">{{ entity.stats.users }}</div>
                  </div>

                </ion-col>

                <ion-col size="6">

                  <div class="stat">
                    <ion-icon class="icon" :icon="trendingUpOutline"></ion-icon>
                    <div class="text">{{ entity.stats.posts }}</div>
                  </div>

                </ion-col>

              </ion-row>

            </div>

          </ion-card>
        </div>
      </div>

      <!-- <div v-if="!loading && !entities.length" class="ion-text-center ion-padding">
        Entity not found.
      </div> -->
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonSearchbar, useIonRouter, IonIcon, IonRow, IonCol, IonCard  } from '@ionic/vue'
import { personOutline, trendingUpOutline } from 'ionicons/icons'
import { EntityType } from '@/utils/interfaces'
import { reactive, computed } from 'vue';
import { useEntityStore } from '@/stores/entity'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'


const ionRouter = useIonRouter()
const entity = useEntityStore()
const user = useUserStore()
const auth = useAuthStore()

const state = reactive({
  search: ''
})

const entities = computed(() => {
  if (state.search) {
    return entity.entities.filter((entity: EntityType) => entity.name.toLowerCase().includes(state.search.toLowerCase()))
  } else {
    return entity.entities
  }
})

function openEntity (entity: EntityType) {
  ionRouter.push(`entity/${entity.id}/posts`)
}

function createEntity () {
  if (!user.success) {
    auth.showMessage('Please log in to create an entity request.', 'info')
    auth.open()
    return
  }
  ionRouter.push('entity/create')
}
</script>

<style lang="scss" scoped>
.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
	grid-gap: 20px;
	grid-auto-rows: auto;
	padding: 15px;
}
.grid-item {
	color: var(--ion-text-color);
	border-radius: 10px;
}
.line {
  border-width: 1px;
}
.search {
  --border-radius: 10px
}
.card {
  border-radius: 7px;
  margin: 0px;
  .title {
    font-size: 18px;
    font-weight: 590;
    color: var(--ion-color-dark);
  }
  .image {
    border-radius: 50%;
    object-fit: cover;
    width: 55px;
    height: 55px;
  }
}
.stat {
  color: var(--ion-color-medium-shade);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 590;

  .icon {
    font-size: 18px;
  }
  
  .text {
    font-size: 16px;
    padding-left: 12px;
  }
}

@media only screen and (max-width: 576px) {
	.grid-container {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		padding: 0px;
		grid-gap: 15px;
	}
	.grid-item {
		padding: 2px 15px;
	}
}

</style>