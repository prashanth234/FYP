<template>

  <ion-page>
    <ion-content>
        
      <ion-modal :is-open="state.isOpen">
        <create-post v-if="state.editPost" :post="state.editPost" @close="closeEditPost($event)" type="edit" />
      </ion-modal>

        <ion-grid v-if="!loading">
          <ion-row class="ion-justify-content-center" v-for="(post, index) in result.myPosts" :key="index">
            <ion-col size="4">
              <post :post="post" :show-edit="true" @editPost="editPost(post, index)" @deletePost="deletePost(post, index)"></post>
            </ion-col>
          </ion-row>
        </ion-grid>

    </ion-content>
  </ion-page>

</template>  

<script setup lang="ts">

import { watch, reactive } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonModal } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue';

const { result, loading } = useQuery(gql`
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
                            `)

watch(result, value => {
  console.log(value)
})

interface PostFileType {
  file: string
}

interface Post {
  id: number,
  description: string,
  postfileSet: PostFileType[]
}

interface State {
  isOpen: boolean,
  editPost: Post | null
}

const state:State = reactive({
  isOpen: false,
  editPost: null
})

function editPost(post: Post, index: number) {
  state.editPost = post
  state.isOpen = true
}

function deletePost(post: Post, index: number) {

}

function closeEditPost(post?: Post) {
  if (post) {
    console.log(post)
  }
  state.isOpen = false
}
</script>