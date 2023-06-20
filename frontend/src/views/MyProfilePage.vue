<template>

  <ion-page>
    <ion-content>
        
      <ion-modal class="edit-post-modal" :is-open="state.isOpen" :show-backdrop="true" @willDismiss="closeEditPost">
        <create-post
          :fixed-preview-height="true"
          :showHeader="true"
          :post="state.editPost"
          @close="closeEditPost"
          @updatePost="updatePost"
          type="edit"
        />
      </ion-modal>

      <ion-modal class="delete-post-modal" :is-open="state.openDialog" :show-backdrop="true" @willDismiss="closeDialog">
        <ion-card style="width: 300px">
          <ion-card-content>
            <ion-row>
              <ion-col size="12" class="delete-message">
                <ion-row>
                  <ion-col size="auto">
                    <ion-icon :icon="warningOutline" color="warning" size="large"></ion-icon>
                  </ion-col>
                  <ion-col style="padding-top: 10px;">
                    <strong> Confirm Delete? </strong>
                  </ion-col>
                </ion-row>
              </ion-col>
              <ion-col size="12">
                <ion-button
                  size="small"
                  color="danger"
                  @click="deletePost"
                  style="float: right"
                >
                  Delete
                </ion-button>
                <ion-button
                  size="small"
                  @click="closeDialog"
                  color="light"
                  style="float: right; margin-right: 15px;"
                >
                  Cancel
                </ion-button>
              </ion-col>
            </ion-row>
          </ion-card-content>
        </ion-card>
      </ion-modal>

      <ion-grid>
        <ion-row class="ion-justify-content-center" >
          <ion-col size="12">
            <ion-row>
              <ion-col size="auto">
                <file-upload-container
                  v-model="state.image"
                  @update:preview="imageSelected"
                  :key="state.refreshFileUpload"
                  :simple="true"
                  :cropable="false"
                >
                  <template #handler="{selectImage}">
                    <ion-avatar style="width: 90px; height: 90px;" class="cpointer" @click="selectImage">
                      <img
                        alt="https://ionicframework.com/docs/img/demos/avatar.svg"
                        src="https://ionicframework.com/docs/img/demos/avatar.svg" 
                      />
                    </ion-avatar>
                    <div class="camera-icon">
                      <ion-icon :icon="cameraOutline"></ion-icon>
                    </div>
                  </template>  
                </file-upload-container>
              </ion-col>
              <ion-col style="margin-top: 10px; margin-left: 10px">
                <h1>Prashanth Bodduna</h1>
              </ion-col>
            </ion-row>
          </ion-col>
          <ion-col>
            <ion-card>
              <ion-segment @ionChange="tabChanged">
                <ion-segment-button value="about">
                  <ion-label>About</ion-label>
                </ion-segment-button>
                <ion-segment-button value="password">
                  <ion-label>Change Password</ion-label>
                </ion-segment-button>
              </ion-segment>

              <ion-card-content>
                <about v-if="state.selectedTab == 'about'" />
                <change-password v-else />
              </ion-card-content>
            </ion-card>
          </ion-col>  
          <ion-col size="7">
            <h5>My Posts</h5>
            <div
              v-for="(post, index) in posts?.myPosts?.posts"
              :key="post.id"
              style="padding: 10px;"
            >
              <post
                :post="post"
                :show-edit="true"
                @editPost="editPost(post, index)"
                @deletePost="confirmDelete(post, index)"
              >
              </post>
            </div>
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
import { IonAvatar, IonSegment, IonSegmentButton, IonLabel, IonCard, IonCardContent, IonIcon, IonButton, IonPage, IonContent, IonCol, IonGrid, IonRow, IonModal, IonInfiniteScroll, IonInfiniteScrollContent, SegmentCustomEvent } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import About from '@/components/aboutContainer.vue'
import ChangePassword from '@/components/changePasswordContainer.vue'
import { useMutation, useQuery } from '@vue/apollo-composable'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { getPosts } from '@/composables/posts'
import { warningOutline, cameraOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'

interface State {
  isOpen: boolean,
  editPost: PostType | null
  openDialog: boolean,
  selectedTab: string | undefined,
  image: null,
  preview: string,
  refreshFileUpload: number
}

interface QueryResult {
  myPosts: {
    posts: PostType[],
    total: number
  }
}

const state: State = reactive({
  isOpen: false,
  editPost: null,
  openDialog: false,
  selectedTab: 'about',
  image: null,
  preview: '',
  refreshFileUpload: 0
})

const { POST_QUERY: MYPOSTS_QUERY, variables, posts, loading, getMore, refetch } = getPosts('myPosts', undefined, undefined)

// Delete Post

function deletePost() {

  try {
    const { mutate, onDone } = useMutation(gql`    
      
      mutation ($id: ID!) { 
        deletePost (
          id: $id,
        ) {
            success
          } 
      }
    `,
      () => ({
        variables: {id: deletePostObj?.id},
        // update: (cache) => {
        //   let data = cache.readQuery<QueryResult>({ query: MYPOSTS_QUERY, variables: CACHE_VARIABLES })
        //   console.log(deletePostObj)
        //   if (!data) { return }
        //   const updatedData = {
        //     ...data,
        //     myPosts: {
        //       ...data.myPosts,
        //       posts: data.myPosts.posts.filter((post: PostType) => {
        //         console.log(post.id != deletePostObj?.id)
        //         return post.id != deletePostObj?.id
        //       })
        //     }
        //   }
        //   console.log(updatedData)
        //   cache.writeQuery({ query: MYPOSTS_QUERY, data: updatedData })
        // },
      })
    )
    mutate()
    onDone((value) => {
      closeDialog()
      variables.page = 1
      refetch()
    })
  } catch (error) {
    console.error(error)
  }
}

let deletePostObj:PostType | null = null

function confirmDelete(post: PostType, index: number) {
  state.openDialog = true
  deletePostObj = post
}

function closeDialog() {
  state.openDialog = false
}

// Edit Post

function editPost(post: PostType, index: number) {
  state.editPost = post
  state.isOpen = true
}

function updatePost(updateVariables: updatePostVariables) {
  try {
    const { mutate, onDone } = useMutation(gql`    
      
      mutation ($id: ID!, $file: Upload, $description: String) { 
        updatePost (
          id: $id,
          file: $file,
          description: $description
        ) {
            post {
              id, 
              likeCount,
              userLiked,
              description,
              postfileSet {
                file
              },
              user {
                username
              }
            }
          } 
      }
    `,
      () => ({
        variables: updateVariables,
        // update: (cache, { data: { updatePost } }) => {
        //   let data = cache.readQuery<QueryResult>({ query: MYPOSTS_QUERY, variables: CACHE_VARIABLES })
        //   if (!data) { return }
        //   data.myPosts.posts.map((post: PostType) => {
        //     if (post.id == updatePost.post.id) {
        //       return updatePost.post
        //     } else {
        //       return post
        //     }
        //   })
        //   console.log(data.myPosts.posts)
        //   cache.writeQuery({ query: MYPOSTS_QUERY, data })
        // },
      })
    )
    mutate()
    onDone((value) => {
      closeEditPost()
    })
  } catch (error) {
    console.error(error)
  }
}

function closeEditPost() {
  state.isOpen = false
}

// Profile Information

function tabChanged(event: SegmentCustomEvent) {
  state.selectedTab = event.target.value
}

// Profile image

function imageSelected() {
  
}
</script>

<style lang="scss" scoped>
  .delete-post-modal {
    --max-width: 350px;
  }
  .edit-post-modal {
    --max-width: 600px;
  }
  .delete-message {
    font-size: 17px;
    color: var(--ion-color-dark);
  }
  .camera-icon {
    position: relative;
    left: 58px;
    bottom: 25px;
    background-color: white;
    color: black;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 50%;
    padding: 6px;
  }
</style>