<template>

  <ion-page>
    <ion-content>
        
      <ion-grid>
        <ion-row>

          <!-- Edit user details -->
          <ion-col size="5" size-xs="12" size-sm="12" size-md="6" size-lg="5" size-xl="4" style="padding: 0px;">
            <ion-card class="profile-card">
              <ion-segment value="about" @ionChange="tabChanged">
                <ion-segment-button value="about">
                  <ion-label>About</ion-label>
                </ion-segment-button>
                <!-- <ion-segment-button value="password">
                  <ion-label>Change Password</ion-label>
                </ion-segment-button> -->
              </ion-segment>

              <ion-card-content>
                <div v-show="state.selectedTab == 'about' ">
                  <about />
                </div>
                <!-- <div  v-show="state.selectedTab == 'password' " >
                  <change-password />
                </div> -->
              </ion-card-content>
              
            </ion-card>
          </ion-col> 

          <!-- User posts -->
          <ion-col size="7" size-xs="12" size-sm="12" size-md="6" size-lg="7" size-xl="8">

            <Feed
              :type="store.type"
              :posts="posts"
              :fetchMoreCompleted="fetchMoreCompleted"
              :fetchMore="fetchMore"
              :refetch="refetch"
              :deleteCntrl="true"
              :editCntrl="true"
              title="My Posts"
              noPostsMsg="The creativity spotlight is ready for you! We'd love to see your unique posts bring this space to life."
            />

          </ion-col>
          
        </ion-row>
      </ion-grid>

    </ion-content>
  </ion-page>

</template>  

<script setup lang="ts">

import { reactive } from 'vue'
import { IonSegment, IonSegmentButton, IonLabel, IonCard, IonCardContent, IonPage, IonContent, IonCol, IonGrid, IonRow, SegmentCustomEvent, SegmentValue } from '@ionic/vue';
import About from '@/components/AboutContainer.vue'
import { scrollTop } from '@/composables/scroll'
import { useProfileInfoStore } from '@/stores/profileInfo'
import Feed from '@/components/FeedContainer.vue'
import { feed } from '@/composables/feed'

scrollTop()

interface State {
  selectedTab: SegmentValue | undefined
}

const state: State = reactive({
  selectedTab: 'about'
})

const store = useProfileInfoStore()

const {
  posts,
  fetchMoreCompleted,
  fetchMore,
  refetch
} = feed(store, undefined)

// Profile Information

function tabChanged(event: SegmentCustomEvent) {
  state.selectedTab = event.target.value
}

</script>

<style lang="scss" scoped>
  .profile-card {
    margin: 5px;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
  }
</style>