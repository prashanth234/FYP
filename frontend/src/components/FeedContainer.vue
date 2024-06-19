<template>

  <ion-row>

    <!-- Feed Header -->
    <ion-col size="12">

      <div class="feed">

        <div class="header">
          Feed
        </div>

        <Refresh
          @refresh="refetch(null)"
          :refreshing="store.refreshing"
        />

        <div style="margin-left: auto;">

          <ion-button
            v-if="store.selectedComptn && !store.selectedComptn.expired"
            :disabled="store.tabSelected == 'trending'"
            @click="onChangeCmptType('trending')"
            style="margin-left: 15px;"
            class="close-button"
            size="small"
            shape="round"
            color="light"
          >
            Trending
          </ion-button>

          <ion-button
            v-if="store.selectedComptn && store.selectedComptn.expired"
            :disabled="store.tabSelected == 'winners'"
            @click="onChangeCmptType('winners')"
            style="margin-left: 15px;"
            class="close-button"
            size="small"
            shape="round"
            color="light"
          >
            Winners
          </ion-button>

          <ion-button
            v-if="store.selectedComptn"
            :disabled="!store.selectedComptn || store.tabSelected == 'allposts'"
            @click="onChangeCmptType('allposts')"
            class="close-button"
            size="small"
            shape="round"
            color="light"
          >
            All
          </ion-button>

        </div>
      </div>

    </ion-col>

    <!-- Notes -->
    <ion-col size="12"
      v-if="noteMessage"
    >

      <alert
        :message="noteMessage"
        class="ion-text-center"
        type="light"
      />

    </ion-col>

    <!-- Posts -->
    <ion-col size="12" class="ion-no-padding posts-content">

      <ion-row>

        <!-- Single post -->
        <ion-col size="12"
          v-if="store.singlePost && store.details.id"
        >
          <SinglePost
            :params="store.getSinglePostParams"
            @more="store.hideSinglePost(true)"
          />
        </ion-col>

        <!-- No posts message -->
        <ion-col size="12"
          class="text-bold ion-text-center ion-padding"
          v-else-if="noPosts"
        >
          There are no posts here yet, be the first to share you're creative content.
        </ion-col>

        <!-- Display the posts -->
        <ion-col size="12"
          v-else
          v-for="post in posts.posts"
          :key="post.id"
        >
          <post :post="post" :position="post.winner?.position"></post>
        </ion-col>

      </ion-row>

      <ion-infinite-scroll 
        :disabled="store.singlePost || fetchMoreCompleted"
        :key="`${fetchMoreCompleted}`"
        @ionInfinite="fetchMore"
        :threshold="user.success ? '400px' : '30px'"
      >
        <ion-infinite-scroll-content loading-text="Loading..." loading-spinner="bubbles"></ion-infinite-scroll-content>
      </ion-infinite-scroll>

    </ion-col>

  </ion-row>

</template>

<script lang="ts" setup>
import Refresh from '@/components/RefreshContainer.vue'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { useEntityInfoStore } from '@/stores/entityInfo'
import { IonButton, IonCol, IonRow, IonInfiniteScroll, IonInfiniteScrollContent } from '@ionic/vue'
import { useUserStore } from '@/stores/user'
import alert from './AlertContainer.vue'
import Post from '@/components/PostContainer.vue'
import SinglePost from '@/components/SinglePostContainer.vue'
import { computed } from 'vue'


const props = defineProps(['type', 'posts', 'fetchMoreCompleted', 'fetchMore', 'refetch', 'onChangeCmptType'])
const store = props.type == 'entity' ? useEntityInfoStore()  : useCategoryInfoStore()
const user = useUserStore();

const noteMessage = computed(() => {
  if (store.selectedComptn?.expired) {
    return 'The contest has concluded! Please take a look at our other ongoing contests.'
  } else if (store.tabSelected == 'trending') {
    if (props.posts.posts?.length) {
      return "Can't spot any trending posts? Be the one who sparks a new wave! Unlock the path to trendiness with just 5 likes for your post!"
    } else {
      return "Contest's top 5 posts with at least 5 likes are currently trending here!"
    }
  }
  return ''
})

const noPosts = computed(() => {
  return !props.posts.posts?.length
})
</script>

<style lang="scss">
.close-button {
  float: right;
  margin: 0px;
}
.posts-content {
  min-height: 500px;
}
.feed {
  display: flex;
  flex-wrap: nowrap;
  padding: 5px;
  .header {
    font-size: 18px;
    font-weight: 580;
  }
}
</style>

