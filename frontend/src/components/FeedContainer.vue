<template>

  <ion-row>

    <!-- Feed Header -->
    <ion-col size="12">

      <div class="feed">

        <div class="header">
          {{ props.title || "Feed" }}
        </div>

        <!-- Popup to edit the post -->
        <ion-modal
          v-if="props.editCntrl"
          class="edit-post-modal"
          :is-open="postDialog.state.isOpen"
          :show-backdrop="true"
          @willDismiss="postDialog.close"
        >
          <create-post
            :fixed-preview-height="true"
            :showHeader="true"
            :post="state.editPost"
            @close="postDialog.close"
            @postUpdated="postDialog.postUpdated"
            type="edit"
          />
        </ion-modal>

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

        <!-- Display the posts -->
        <ion-col size="12"
          v-else-if="!noPosts"
          v-for="(post, index) in posts.posts"
          :key="post.id"
        >
          <post
            :post="post"
            :position="store.tabSelected == 'winners' ? index + 1 : undefined"
            :show-by-owner-tag="props.showByOwnerTag"
            :show-from-entity-tag="props.showFromEntityTag"
            :show-edit="props.editCntrl"
            :show-delete="props.deleteCntrl"
            @editPost="editPost(post, index)"
            @deletePost="confirmDelete(post, index)"
          ></post>
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
import { useProfileInfoStore } from '@/stores/profileInfo'
import { IonModal, IonButton, IonCol, IonRow, IonInfiniteScroll, IonInfiniteScrollContent } from '@ionic/vue'
import { useUserStore } from '@/stores/user'
import alert from './AlertContainer.vue'
import Post from '@/components/PostContainer.vue'
import SinglePost from '@/components/SinglePostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { computed, reactive } from 'vue'
import { usePostDialog } from '@/composables/postDialog'
import { useDialogStore } from '@/stores/dialog'
import { PostType } from '@/utils/interfaces'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { warningOutline } from 'ionicons/icons'
import { useToastStore } from '@/stores/toast'

const props = defineProps([
  'type',
  'posts',
  'fetchMoreCompleted',
  'fetchMore',
  'refetch',
  'onChangeCmptType',
  'title',
  'noPostsMsg',
  'deleteCntrl',
  'editCntrl',
  'showByOwnerTag',
  'showFromEntityTag'
])

const store = props.type == 'entity' ? useEntityInfoStore()  : (props.type == 'profile' ? useProfileInfoStore() : useCategoryInfoStore())
const user = useUserStore();
const postDialog = usePostDialog();
const dialog = useDialogStore();
const toast = useToastStore();

interface State {
  editPost: PostType | null | undefined,
}

const state: State = reactive({
  editPost: null
})

const noPosts = computed(() => {
  return !props.posts.posts?.length
})

const noteMessage = computed(() => {
  if (store.selectedComptn?.expired) {
    return 'The contest has concluded! Please take a look at our other ongoing contests.'
  } else if (store.tabSelected == 'trending') {
    return "Share your post with friends and family to reach 5 likes and get featured!"
  } else if (noPosts.value) {
    return props.noPostsMsg || "There are no posts here yet, be the first to share you're creative content."
  }
  return ''
})

////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Performing deletion and edit post in feed container to make post container as light weight as possible
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Delete Post

function deletePost() {

  const id = deletePostObj?.id

  const { mutate, onDone, onError } = useMutation(gql`    
    
    mutation ($id: ID!) { 
      deletePost (
        id: $id,
      ) {
          success,
          caId,
          entity {
            id,
            stats {
              posts,
              categories {
                count
              }
            }
          }
        } 
    }
  `,
    () => ({
      variables: {id},
      update: (cache, { data: { deletePost } }) => {
        const normalizedPostId = cache.identify({ id, __typename: 'PostType' });
        cache.evict({ id: normalizedPostId })
        if (deletePost.caId) {
          // Delete the coin activity cache
          const normalizedCAId = cache.identify({ id: deletePost.caId, __typename: 'CoinActivitiesType' });
          cache.evict({ id: normalizedCAId })
        }
        cache.gc()
      }
    })
  )

  mutate()

  onDone((value) => {
    dialog.close()
    toast.$patch({message: 'Success! The post has been deleted.', color: 'success', open: true})
  })

  onError((error: any) => {
    toast.$patch({message: "Apologies, but we couldn't delete the post due to an error.", color: 'danger', open: true})
  })
}

let deletePostObj:PostType | null = null

function confirmDelete(post: PostType, index: number) {
  const buttons = [
    {title: 'Delete', color: 'danger', action: 'delete', control: deletePost},
    {title: 'Cancel', color: 'light'}
  ]
  dialog.show('Confirm Delete?', '', buttons, warningOutline, 'warning')
  deletePostObj = post
}

// Edit Post

function editPost(post: PostType, index: number) {
  state.editPost = post
  postDialog.open()
}
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
@media only screen and (min-width: 576px) {
  .edit-post-modal {
    --max-width: 600px !important;
    --height: auto;
  }
}
.edit-post-modal {
  // For xs screens
  --max-width: 100%;
}
</style>

