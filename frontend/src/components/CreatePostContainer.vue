<template>

    <div>

      <ion-toolbar color="light">
        <ion-title>{{ state.title }}</ion-title>
        <ion-buttons slot="end">
          <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="emit('close')"></ion-icon>
        </ion-buttons>
      </ion-toolbar>

      <ion-grid style="padding: 10px">
        <ion-row>

          <ion-col size="12" class="ion-no-padding">

            <ion-row v-if="type=='create'">
              <ion-col size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6" >
                <ion-select
                  class="custom-select"
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

              <ion-col size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6">
                <ion-select
                  class="custom-select"
                  v-model="state.entity"
                  placeholder="Select"
                  label="Entity"
                  interface="popover"
                >
                  <ion-select-option
                    v-for="entity in entity.entities"
                    :key="entity.id"
                    :value="entity"
                  >
                    {{ entity.name }}
                  </ion-select-option>
                </ion-select>

              </ion-col>

              <ion-col size="12">
                <ion-select
                  class="custom-select"
                  v-model="state.competition"
                  placeholder="Select"
                  label="Contest"
                  interface="popover"
                >
                  <ion-select-option value="">
                    None
                  </ion-select-option>
                  <ion-select-option
                    v-for="competition in state.catCompetitions"
                    :key="competition.id"
                    :class="{'competition-expired': competition.expired}"
                    :value="competition.id"
                  >
                    {{ competition.name }}
                  </ion-select-option>
                </ion-select>
              </ion-col>

              <ion-col
                v-if="state.competition && !state.entity.ispublic && state.entity.userAccess == 'SUCCESS'"
                class="ion-text-start"
                style="color: var(--ion-color-warning);"
              >
                Selected entity is private. Posting in the contest makes post public.
              </ion-col>

            </ion-row>

          </ion-col>

         

          <ion-col size="12" class="content-container">
            <ion-textarea
              label-placement="stacked"
              v-model="state.description"
              placeholder="Describe your post."
              :auto-grow="true"
              class="custom-textarea"
            />
            <div style="width: 100%; margin-top: 15px;" v-if="showImageUpload && state.preview">
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
              <template #handler="{selectImage, loading}">
                <ion-row class="padding-col-zero">
                  <ion-col size="auto" v-if="showImageUpload">
                    <ion-button
                      @click="selectImage()"
                      for="file-upload"
                      size="small"
                      color="primary"
                      :disabled="loading || state.creatingPost"
                    >
                      <ion-spinner 
                        class="button-loading-small"
                        v-if="loading"
                        name="crescent"
                      />
                      <span v-else>
                        {{ state.preview ? 'Change Image' : 'Select Image' }}
                      </span>
                    </ion-button>
                  </ion-col>
                  <ion-col>
                    <ion-button
                      size="small"
                      @click="state.uploadAction"
                      :disabled="disableUpload || loading"
                      class="float-right"
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
                  </ion-col>
                </ion-row>
              </template>  
            </file-upload-container>
          </ion-col>

        </ion-row>
      </ion-grid>

    </div>

</template>

<script lang="ts" setup>
import { useIonRouter, IonSelect, IonSelectOption, IonHeader, IonToolbar, IonTitle, IonButtons, IonIcon, IonTextarea, IonCard, IonSpinner, IonButton, IonCol, IonGrid, IonRow, IonImg } from '@ionic/vue';
import { useRoute } from 'vue-router';
import { closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive, computed } from 'vue'
import { CompetitionInfo, EntityType } from '@/utils/interfaces'
import { useToastStore } from '@/stores/toast'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { useUserStore } from '@/stores/user'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useCategoryStore } from '@/stores/category'
import { useEntityStore } from '@/stores/entity'
import { useQuery } from '@vue/apollo-composable'
import { getQuery, POST_COMMON_FIELDS } from '@/composables/posts'
import { getQuery as getCoinActivityQuery, CoinActivities } from '@/composables/coinActivity'
import { useAuthStore } from '@/stores/auth'

interface PostFileType {
  file: string,
  files: {
    lg: string,
    md: string,
    og: string
  }
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
  [key: string]: {
    posts: PostType[],
    total: number
  }
}

interface VariablesType {
  [key: string]: {
    category?: string,
    competition?: string,
    entity?: string,
    trending?: boolean,
  }
}

interface CachesType {
  category: AllPostsType | null,
  competition: AllPostsType | null,
  trending: AllPostsType | null,
  profile: AllPostsType | null,
  entity: AllPostsType | null
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
  entity: {} as EntityType,

  catCompetitions: [] as CompetitionInfo[],
  preview: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  creatingPost: false,
  uploadAction: () => {}
})

const disableUpload = computed(() => {
  return (showImageUpload.value && !state.preview) || (props.type == 'create' && !state.category) || state.creatingPost || (postType.value == 'TEXT' && !state.description)
})

const showImageUpload = computed(() => {
  return postType.value == 'IMAGETEXT'
})

const postType = computed(() => {
  // Post edit we have oftype information on post itself
  if (props.post) { return props.post.category.oftype }

  // Post create we have oftype information using the category id
  const selectedCategory = category.categories.find(cat => cat.id === state.category)
  if (selectedCategory) {
    if (selectedCategory.oftype == 'TEXT') {
      state.image = null
      state.preview = ''
    }
    return selectedCategory.oftype
  }

  return ''
})

const ionRouter = useIonRouter();
const router = useRoute();

const toast = useToastStore()
const user = useUserStore()
const category = useCategoryStore()
const entity = useEntityStore()
const auth = useAuthStore()
// category.getCategories()

const { QUERY: POST_QUERY } = getQuery('allPosts')
const { QUERY: MYPOSTS_QUERY } = getQuery('myPosts')
const { QUERY: ENTITYPOSTS_QUERY } = getQuery('entityPosts')

if (props.type == 'create') {
  // Intialize create post data
  const { id, selectedComptn } = useCategoryInfoStore()
  state.category = id
  if (id) {
    onCategoryChange()
  }
  state.competition = !selectedComptn?.expired && selectedComptn?.id ? selectedComptn.id : ''
}

function clearPostForm () {
  state.preview = ''
  state.image = null
  state.description = ''
  state.refreshFileUpload++
}

function onCategoryChange() {
  state.catCompetitions = []
  state.competition = ''

  const { onResult, onError } = useQuery(gql`
                                  query ($id: ID!) {
                                    catCompetitions (id: $id) {
                                      name,
                                      id,
                                      expired
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
    auth.open()
    return
  }

  // Check if user part of entity 
  if (state.entity.userAccess == 'NOTFOUND') {
    toast.$patch({message: `You're not part of ${state.entity.name} entity. Please join the entity to post in it.`, color: 'primary', open: true})
    return
  } 

  // Description check for short stories
  if (postType.value == "TEXT") {
    const wordcount =  state.description.split(/\s+/).length
    if (wordcount < 100 || wordcount > 1000) {
      toast.$patch({message: 'Stories should be between 100 to 1000 words. Keep it concise and captivating!', color: 'warning', open: true})
      return
    } 
  }

  state.creatingPost = true

  let postVariables = {
    file: state.image || undefined,
    description: state.description,
    competition: state.competition || undefined,
    category: state.category,
    entity: state.entity.id
  }

  const { mutate, onDone, error: sendMessageError, onError } = useMutation(gql`    
    
    mutation ($file: Upload, $category: ID, $competition: ID, $description: String!, $entity: ID!) { 
      createPost (
        file: $file,
        competition: $competition,
        category: $category,
        description: $description,
        entity: $entity
      ) {
          post {
            ${POST_COMMON_FIELDS},
            competition {
              expired
            },
            isBot
          },
          coinActivity {
            id,
            points,
            description,
            status,
            createdAt
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
          entity: {entity: state.entity.id},
          profile: {trending: false}
        }

        let caches: CachesType = {
          category: cache.readQuery({ query: POST_QUERY, variables: variables.category }),
          competition: null,
          trending: null,
          profile: cache.readQuery({query: MYPOSTS_QUERY, variables: variables.profile }),
          entity: cache.readQuery({query: ENTITYPOSTS_QUERY, variables: variables.entity })
        }

        if (state.competition) {
          caches.competition = cache.readQuery({ query: POST_QUERY, variables: variables.competition })
          caches.trending = cache.readQuery({ query: POST_QUERY, variables: variables.trending })

          // Update coin activities cache
          const COINACTIVITY_QUERY = getCoinActivityQuery()
          const caCache: CoinActivities | null = cache.readQuery({query: COINACTIVITY_QUERY})
          if (caCache) {
            const data = {
              ...caCache,
              coinactivities: [
                createPost.coinActivity,
                ...caCache.coinactivities
              ]
            }
            cache.writeQuery({ query: COINACTIVITY_QUERY, data })
          } 
        }

        function updatePosts(type: string, data: AllPostsType, addAtEnd: boolean = false) {
          const start = [], end = []
          addAtEnd ? end.push(createPost.post) : start.push(createPost.post)

          return {
            ...data,
            [type]: {
              ...data[type],
              posts: [
                ...start,
                ...data[type].posts,
                ...end
              ]
            }
          }
        }

        for (let [key, data] of Object.entries(caches)) {
          if (data) {

            if (key == 'profile') {
              data = updatePosts('myPosts', data)
              cache.writeQuery({ query: MYPOSTS_QUERY, data, variables: variables[key] })
              continue
            } else if (key == 'trending') {
              if (data.allPosts.posts.length >= 5) { continue }
              data = updatePosts('allPosts', data, true)
            } else if (key == 'entity') {
              data = updatePosts('entityPosts', data)
              cache.writeQuery({ query: ENTITYPOSTS_QUERY, data, variables: variables[key] })
              continue
            } else {
              data = updatePosts('allPosts', data)
            }

            cache.writeQuery({ query: POST_QUERY, data, variables: variables[key] })
          }
        }

      },
    })
  )

  mutate()

  onDone(() => {
    if (state.entity.userAccess == 'PENDING') {
      toast.$patch({message: "Post uploaded. It'll show in the entity once your join entity request is verified.", color: 'success', open: true})
    } else {
      toast.$patch({message: 'Success! Your post has been uploaded.', color: 'success', open: true})
    }
    state.creatingPost = false
    clearPostForm()
    emit('postCreated')
    const routeToPath = `/interests/${state.category}/posts`
    routeToPath != router.path && ionRouter.push(routeToPath)
  })

  onError((error: any) => {
    state.creatingPost = false
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else if (error?.graphQLErrors) {
      toast.$patch({message: error?.graphQLErrors[0].message, color: 'primary', open: true})
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
    state.creatingPost = true

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
                files {
                  lg,
                  md,
                  og
                },
                width,
                height
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
      toast.$patch({message: 'Success! Your post has been updated.', color: 'success', open: true})
      state.creatingPost = false
      emit('postUpdated')
    })

    onError((error: any) => {
      state.creatingPost = false
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
    props.post.postfileSet.length && (state.preview = props.post.postfileSet[0].files.og )
    state.uploadAction = updatePost
  } else if (props.type == 'create') {
    state.title = 'Create Post'
    state.uploadTitle = 'Upload'
    state.uploadAction = createNewPost
  }
}

initialize()
</script>

<style scoped lang="scss">
.textarea {
  border: 1px solid #dddfe2;
}
.preview-image {
  height: 250px;
  overflow: auto;
}
.content-container {
  margin-top: 10px;
  padding-top: 0px;
  max-height: calc(100vh - 225px);
  overflow-y: auto;
}
@media only screen and (max-width: 576px) {
	// For xs
  .content-container {
    max-height: calc(100vh - 350px);
  }
}
</style>
<style>
.competition-expired {
  display: none;
}
</style>