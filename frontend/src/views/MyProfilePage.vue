<template>

  <ion-page>
    <ion-content>
        
      <ion-modal class="edit-post-modal" :is-open="postDialog.state.isOpen" :show-backdrop="true" @willDismiss="postDialog.close">
        <create-post
          :fixed-preview-height="true"
          :showHeader="true"
          :post="state.editPost"
          @close="postDialog.close"
          @postUpdated="postDialog.postUpdated"
          type="edit"
        />
      </ion-modal>
      
      <common-dialog @action="$event => $event.control()"></common-dialog>

      <ion-grid>
        <ion-row>
          <ion-col size="5" size-xs="12" size-sm="12" size-md="6" size-lg="5" size-xl="4">
            <ion-card>
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
          <ion-col size="7" size-xs="12" size-sm="12" size-md="6" size-lg="7" size-xl="8">
            <h5 class="ion-padding-start">My Posts</h5>
            <ion-row class="ion-justify-content-center">
              <ion-col
                v-for="(post, index) in posts?.myPosts?.posts"
                :key="post.id"
                size="7" size-xs="12" size-sm="12" size-md="10" size-lg="8" size-xl="7"
              >
                <post
                  :post="post"
                  :show-edit="true"
                  @editPost="editPost(post, index)"
                  @deletePost="confirmDelete(post, index)"
                >
                </post>
              </ion-col>
            </ion-row>
          </ion-col>
        </ion-row>
      </ion-grid>

      <ion-infinite-scroll @ionInfinite="getMore">
        <ion-infinite-scroll-content></ion-infinite-scroll-content>
      </ion-infinite-scroll>

    </ion-content>
  </ion-page>

</template>  

<script setup lang="ts">

import { reactive } from 'vue'
import gql from 'graphql-tag'
import { IonSegment, IonSegmentButton, IonLabel, IonCard, IonCardContent, IonIcon, IonButton, IonPage, IonContent, IonCol, IonGrid, IonRow, IonModal, IonInfiniteScroll, IonInfiniteScrollContent, SegmentCustomEvent, SegmentValue } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import About from '@/components/AboutContainer.vue'
// import ChangePassword from '@/components/changePasswordContainer.vue'
import { useMutation, useQuery } from '@vue/apollo-composable'
import { UpdatePostVariables, Post as PostType } from '@/utils/interfaces'
import { getPosts } from '@/composables/posts'
import { warningOutline } from 'ionicons/icons'
import { CropperResult } from 'vue-advanced-cropper'
import { useToastStore } from '@/stores/toast'
import { usePostDialog } from '@/composables/postDialog'
import { useDialogStore } from '@/stores/dialog';
import CommonDialog from '@/components/CommonDialogContainer.vue';
import { scrollTop } from '@/composables/scroll'

scrollTop()

interface State {
  editPost: PostType | null | undefined,
  selectedTab: SegmentValue | undefined
}

interface QueryResult {
  myPosts: {
    posts: PostType[],
    total: number
  }
}

const state: State = reactive({
  editPost: null,
  selectedTab: 'about'
})

const toast = useToastStore()
const postDialog = usePostDialog()
const dialog = useDialogStore()

const { POST_QUERY: MYPOSTS_QUERY, variables, posts, loading, getMore, refetch } = getPosts('myPosts')

// Delete Post

function deletePost() {

  const id = deletePostObj?.id

  const { mutate, onDone, onError } = useMutation(gql`    
    
    mutation ($id: ID!) { 
      deletePost (
        id: $id,
      ) {
          success
        } 
    }
  `,
    () => ({
      variables: {id},
      update: (cache) => {
        const normalizedId = cache.identify({ id, __typename: 'PostType' });
        cache.evict({ id: normalizedId })
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

// Profile Information

function tabChanged(event: SegmentCustomEvent) {
  state.selectedTab = event.target.value
}

</script>

<style lang="scss" scoped>
  @media only screen and (min-width: 576px) {
    .edit-post-modal {
      --max-width: 600px;
    }
  }
  .edit-post-modal {
    --max-width: 90%;
    --height: auto;

    &::part(content) {
      background: none;
      box-shadow: none;
    }
  }
</style>