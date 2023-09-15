<template>

    
    <ion-card class="padding-zero margin-zero border-radius-std">

      <ion-toolbar color="light">
        <ion-title>{{ state.title }}</ion-title>
        <ion-buttons slot="end">
          <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="emit('close')"></ion-icon>
        </ion-buttons>
      </ion-toolbar>

      <ion-grid style="padding: 10px">
        <ion-row>

          <ion-col size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6" v-if="type=='create'">
            <ion-select
              fill="outline"
              class="custom-input"
              v-model="state.category"
              placeholder="Select"
              label="Interest"
              interface="popover"
              @ionChange="onCategoryChange"
            >
              <ion-select-option
                v-for="cat in category.categories"
                :key="cat.id"
                :value="cat.id"
              >
                {{ cat.name }}
              </ion-select-option>
            </ion-select>
          </ion-col>

          <ion-col size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6" v-if="type=='create'">
            <ion-select
              class="custom-input"
              v-model="state.competition"
              placeholder="Select"
              fill="outline"
              label="Contest"
              interface="popover"
            >
              <ion-select-option value="">
                None
              </ion-select-option>
              <ion-select-option
                v-for="competition in state.catCompetitions"
                :key="competition.id"
                :value="competition.id"
              >
                {{ competition.name }}
              </ion-select-option>
            </ion-select>
          </ion-col>

          <ion-col size="12">
            <ion-textarea
              label="Description"
              v-model="state.description"
              placeholder="Describe your post"
              :auto-grow="true"
              fill="outline"
            />
          </ion-col>

          <ion-col size="12" v-if="showImageUpload && state.preview">
            <div :class="{'preview-image': props.fixedPreviewHeight}" style="margin: 10px">
              <ion-img :src="state.preview"></ion-img>
            </div>
          </ion-col>

          <ion-col size="12">
            <file-upload-container
              v-model:preview="state.preview"
              v-model="state.image"
              :key="state.refreshFileUpload"
              :simple="true"
              :cropable="false"
            >
              <template #handler="{selectImage}">
                <ion-row class="padding-col-zero">
                  <ion-col size="auto" v-if="showImageUpload">
                    <ion-button
                      @click="selectImage()"
                      for="file-upload"
                      size="small"
                      color="primary"
                    >
                      {{ state.preview ? 'Change Image' : 'Select Image' }}
                    </ion-button>
                  </ion-col>
                  <ion-col>
                    <ion-button
                      size="small"
                      @click="state.uploadAction"
                      :disabled="(showImageUpload && !state.preview) || !!state.creatingPost"
                      style="float: right"
                    >
                      <ion-spinner 
                        class="button-loading-small"
                        v-if="state.creatingPost"
                        name="crescent"
                      />
                      <span v-else>
                        {{ state.uploadTitle }}
                      </span>
                    </ion-button>
                    <ion-button
                      size="small"
                      @click="clearPostForm"
                      color="light"
                      class="ion-padding-end"
                      style="float: right"
                    >
                      Clear
                    </ion-button>
                  </ion-col>
                </ion-row>
              </template>  
            </file-upload-container>
          </ion-col>

        </ion-row>
      </ion-grid>
    </ion-card>

</template>

<script lang="ts" setup>
import { IonSelect, IonSelectOption, IonHeader, IonToolbar, IonTitle, IonButtons, IonIcon, IonTextarea, IonCard, IonSpinner, IonButton, IonCol, IonGrid, IonRow, IonImg } from '@ionic/vue';
import { caretDown, closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive, computed } from 'vue'
import { CompetitionInfo, UpdatePostVariables, categoryObject } from '@/mixims/interfaces'
import { useToastStore } from '@/stores/toast'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { useUserStore } from '@/stores/user'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useCategoryStore } from '@/stores/category';
import { useQuery } from '@vue/apollo-composable'
import { getPosts } from '@/composables/posts'

interface PostFileType {
  file: string
}

interface PostType {
  id: number,
  description: string,
  postfileSet: PostFileType[],
  category: {
    oftype: string
  }
}

interface AllPostsType {
  allPosts?: {
    posts: PostType[],
    total: number
  },
  myPosts?: {
    posts: PostType[],
    total: number
  }
}

interface VariablesType {
  [key: string]: {
    category?: string,
    competition?: string,
    trending: boolean,
  }
}

interface CachesType {
  category: AllPostsType | null,
  competition: AllPostsType | null,
  trending: AllPostsType | null,
  profile: AllPostsType | null
}

const props = defineProps<{
  post?: PostType | null,
  type: string,
  showHeader?: Boolean,
  fixedPreviewHeight: Boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'postUpdated'): void;
  (e: 'postCreated'): void;
}>()

const state = reactive({
  // Post Information
  image: null,
  description: '',
  category: '',
  competition: '',
  oftype: '',

  catCompetitions: [] as CompetitionInfo[],
  preview: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  creatingPost: false,
  uploadAction: () => {}
})

const showImageUpload = computed(() => {
  return state.oftype == 'IMAGETEXT'
})

const toast = useToastStore()
const user = useUserStore()
const category = useCategoryStore()
category.getCategories()

const { POST_QUERY } = getPosts('allPosts', undefined, undefined)
const { POST_QUERY: MYPOSTS_QUERY } = getPosts('myPosts', undefined, undefined)

if (props.type == 'create') {
  // Intialize create post data
  const { oftype, id, selectedComptn } = useCategoryInfoStore()
  state.oftype = oftype
  state.category = id
  state.competition = selectedComptn?.id || ''
  if (id) {
    onCategoryChange()
  }
} else if (props.post){
  // Post edit case
  state.oftype = props.post.category.oftype
}

function clearPostForm () {
  state.preview = ''
  state.image = null
  state.description = ''
  state.refreshFileUpload++
}

function onCategoryChange() {
  state.catCompetitions = []

  const [{oftype}] = category.categories.filter(cat => cat.id === state.category)
  state.oftype = oftype
  state.competition = ''
  if (oftype == 'TEXT') {
    state.image = null
    state.preview = ''
  }

  const { onResult, onError } = useQuery(gql`
                                  query ($id: Int!) {
                                    catCompetitions (id: $id) {
                                      name,
                                      id,
                                    }
                                  }
                                `,
                                  {
                                    id: state.category
                                  }
                                )

  onResult(({data, loading}) => {
    !loading && (state.catCompetitions = data.catCompetitions)
  })
}

function createNewPost() {

  if (!user.success) {
    user.auth = true
    return
  }

  state.creatingPost = true

  let postVariables = {
    file: state.image || undefined,
    description: state.description,
    competition: state.competition || undefined,
    category: state.category
  }

  const { mutate, onDone, error: sendMessageError, onError } = useMutation(gql`    
    
    mutation ($file: Upload, $category: ID, $competition: ID, $description: String!) { 
      createPost (
        file: $file,
        competition: $competition,
        category: $category,
        description: $description
      ) {
          post {
            id,
            likes,
            userLiked,
            description,
            postfileSet {
              file
            },
            user {
              username,
              avatar
            },
            category {
              oftype
            }
          }  
        }
    }

  `, () => ({
      variables: postVariables,
      update: (cache, { data: { createPost } }) => {

        let variables: VariablesType = {
          category: {category: state.category, trending: false},
          competition: {category: state.category, competition: state.competition, trending: false},
          trending: {category: state.category, competition: state.competition, trending: true},
          profile: {trending: false}
        }

        let caches: CachesType = {
          category: cache.readQuery({ query: POST_QUERY, variables: variables.category }),
          competition: null,
          trending: null,
          profile: cache.readQuery({query: MYPOSTS_QUERY, variables: variables.profile })
        }

        if(state.competition) {
          caches.competition = cache.readQuery({ query: POST_QUERY, variables: variables.competition })
          caches.trending = cache.readQuery({ query: POST_QUERY, variables: variables.trending })
        }

        for (let [key, data] of Object.entries(caches)) {
          if (data) {

            if (key == 'profile') {
              data = {
                ...data,
                myPosts: {
                  ...data.myPosts,
                  posts: [
                    createPost.post,
                    ...data.myPosts.posts
                  ]
                }
              }

              cache.writeQuery({ query: MYPOSTS_QUERY, data, variables: variables[key] })
              continue
            } else if (key == 'trending') {
              if (data.allPosts.posts.length >= 5) { continue }
              data = {
                ...data,
                allPosts: {
                  ...data.allPosts,
                  posts: [
                    ...data.allPosts.posts,
                    createPost.post
                  ]
                }
              }
              
            } else {
              data = {
                ...data,
                allPosts: {
                  ...data.allPosts,
                  posts: [
                    createPost.post,
                    ...data.allPosts.posts
                  ]
                }
              }
            }

            cache.writeQuery({ query: POST_QUERY, data, variables: variables[key] })
          }
        }

      },
    })
  )

  mutate()

  onDone(() => {
    state.creatingPost = false
    clearPostForm()
    emit('postCreated')
  })

  onError((error: any) => {
    state.creatingPost = false
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else {
      toast.$patch({message: 'Error Occured While Uploading Post', color: 'danger', open: true})
    }
  })
}

function updatePost() {
  if (!props.post) { return }
  const variables = { id: props.post.id }
  const {description, postfileSet} = props.post

  if (description != state.description) {
    Object.assign(variables, { description: state.description })
  }

  if (state.image && postfileSet[0].file != state.image) {
    Object.assign(variables, { file: state.image })
  }

  if (Object.keys(variables).length == 1) {
    toast.$patch({message: 'No changes made', color: 'warning', open: true})
  } else {
    const { mutate, onDone, onError } = useMutation(gql`    
    
      mutation ($id: ID!, $file: Upload, $description: String) { 
        updatePost (
          id: $id,
          file: $file,
          description: $description
        ) {
            post {
              id,
              description,
              postfileSet {
                file
              },
            }
          }
      }
    `,
      {
        variables
      }
    )
    
    mutate()

    onDone((value) => {
      emit('postUpdated')
    })

    onError((error: any) => {
      if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
        toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
      } else {
        toast.$patch({message: 'Error Occured While Updating Post', color: 'danger', open: true})
      }
    })
  }
}

function initialize() {
  if (props.type == 'edit' && props.post) {
    state.title = 'Edit Post'
    state.uploadTitle = 'Update'
    state.description = props.post.description
    props.post.postfileSet.length && (state.preview = `/media/${props.post.postfileSet[0].file}`)
    state.uploadAction = updatePost
  } else if (props.type == 'create') {
    state.title = 'Create Post'
    state.uploadTitle = 'Upload'
    state.uploadAction = createNewPost
  }
}

initialize()
</script>

<style scoped>
.textarea {
  border: 1px solid #dddfe2;
  /* padding: 20px;
  border-radius: 4px; */
}
.preview-image {
  height: 250px;
  overflow: auto;
}
</style>