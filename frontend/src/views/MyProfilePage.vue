<template>

  <ion-page>
    <ion-content>
        
      <ion-modal :is-open="state.isOpen">
        <create-post v-if="state.editPost" :post="state.editPost" @close="closeEditPost" @updatePost="updatePost" type="edit" />
      </ion-modal>

        <ion-grid>
          <ion-row class="ion-justify-content-center" v-for="(post, index) in posts?.myPosts?.posts" :key="index">
            <ion-col size="4">
              <post :post="post" :show-edit="true" @editPost="editPost(post, index)" @deletePost="deletePost(post, index)"></post>
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
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonModal, IonInfiniteScroll, IonInfiniteScrollContent } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { useMutation } from '@vue/apollo-composable'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { getPosts } from '@/composables/posts'

interface State {
  isOpen: boolean,
  editPost: PostType | null
}

const state:State = reactive({
  isOpen: false,
  editPost: null
})


const MYPOSTS_QUERY = gql`
                          query {
                            myPosts {
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
                        `

const { POST_QUERY, posts, loading, getMore } = getPosts('myPosts')

function editPost(post: PostType, index: number) {
  state.editPost = post
  state.isOpen = true
}

function deletePost(post: PostType, index: number) {

}
function updatePost(variables:updatePostVariables) {
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
        variables,
        update: (cache, { data: { updatePost } }) => {
          let data = cache.readQuery({ query: MYPOSTS_QUERY })
          data.myPosts.map((post: PostType) => {
            if (post.id == updatePost.post.id) {
              return updatePost.post
            } else {
              return post
            }
          })
          cache.writeQuery({ query: MYPOSTS_QUERY, data })
        },
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
// function updatePost(variables:updatePostVariables) {
//   try {
//     const { mutate, onDone } = useMutation(gql`    
      
//       mutation ($id: ID!, $file: Upload, $description: String) { 
//         updatePost (
//           id: $id,
//           file: $file,
//           description: $description
//         ) {
//             post {
//               id, 
//               likeCount,
//               userLiked,
//               description,
//               postfileSet {
//                 file
//               },
//               user {
//                 username
//               }
//             }
//           } 
//       }

//     `,
//       () => ({
//         variables,
//         update: (cache, { data: { updatePost } }) => {
//           let data = cache.readQuery({ query: POST_QUERY })
//           console.log(data, POST_QUERY)
//           data.myPosts.posts.map((post: PostType) => {
//             if (post.id == updatePost.post.id) {
//               return updatePost.post
//             } else {
//               return post
//             }
//           })
//           cache.writeQuery({ query: POST_QUERY, data })
//         },
//       })
//     )

//     mutate()
//     onDone((value) => {
//       closeEditPost()
//     })
//   } catch (error) {
//     console.error(error)
//   }
// }

function closeEditPost() {
  state.isOpen = false
}
</script>