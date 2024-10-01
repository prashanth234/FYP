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

              <ion-col size="12" v-if="state.alertMsg">
                <alert :message="state.alertMsg" type="warning"/>
              </ion-col>
              
              <ion-col size="6" size-xs="12" size-sm="12" size-md="6" size-lg="6" size-xl="6" >
                <ion-select
                  class="custom-select"
                  v-model="state.category"
                  placeholder="Select"
                  label="Interest"
                  interface="popover"
                  @ionChange="getCompetitions"
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
                  @ionChange="getCompetitions"
                >
                  <ion-select-option
                    v-for="ety in entity.entities"
                    :key="ety.id"
                    :value="ety"
                  >
                    {{ ety.name }}
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
                  <ion-select-option disabled class="select-option-header" v-if="state.competitions.globalList.length">
                    Global Contests
                  </ion-select-option>
                  <ion-select-option
                    v-for="competition in state.competitions.globalList"
                    :key="competition.id" :value="competition.id"
                    style="padding-left: 10px;"
                  >
                    {{ competition.name }}
                  </ion-select-option>
                  <ion-select-option disabled class="select-option-header" v-if="state.competitions.entityList.length">
                    Entity's Contests
                  </ion-select-option>
                  <ion-select-option
                    v-for="competition in state.competitions.entityList"
                    :key="competition.id" :value="competition.id"
                  >
                    {{ competition.name }}
                  </ion-select-option>
                </ion-select>
              </ion-col>

              <ion-col
                v-if="
                  state.competition &&
                  !state.entity.ispublic && 
                  isGlobalCompetition
                "
                class="ion-text-start"
                style="color: var(--ion-color-warning);"
              >
                Selected entity is private. Posting in the Global contest makes post public.
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
import { closeOutline, key } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive, computed } from 'vue'
import { CompetitionType, EntityType, PostType } from '@/utils/interfaces'
import { useToastStore } from '@/stores/toast'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { useEntityInfoStore } from '@/stores/entityInfo'
import { useUserStore } from '@/stores/user'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useCategoryStore } from '@/stores/category'
import { useEntityStore } from '@/stores/entity'
import { useQuery } from '@vue/apollo-composable'
import { getQuery, POST_COMMON_FIELDS } from '@/composables/posts'
import { getQuery as getCoinActivityQuery, CoinActivities } from '@/composables/coinActivity'
import { useAuthStore } from '@/stores/auth'
import alert from './AlertContainer.vue'

interface AllPostsType {
  [key: string]: {
    posts: PostType[],
    total: number
  }
}

interface VariablesType {
  category?: string,
  competition?: string,
  entity?: string,
  cpType?: string,
  trending?: boolean
}

interface CacheType {
  [key: string]: {
    variables: VariablesType,
    query: any,
    name: string,
    ignore?: boolean,
    max?: number,
    addEnd?: boolean
  }
}

interface Competitions {
  globalList: CompetitionType[],
  entityList: CompetitionType[]
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

  competitions: {globalList: [], entityList: []} as Competitions,
  preview: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  creatingPost: false,
  uploadAction: () => {},
  alertMsg: ''
})

const disableUpload = computed(() => {
  return (showImageUpload.value && !state.preview) || (props.type == 'create' && !state.category) || state.creatingPost || (postType.value == 'TEXT' && !state.description)
})

const showImageUpload = computed(() => {
  return postType.value == 'IMAGETEXT'
})

const isGlobalCompetition = computed(() => {
  return state.competition && state.competitions.globalList.some(item => item.id == state.competition)
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
const categoryInfo = useCategoryInfoStore()
const entityInfo = useEntityInfoStore()

const { QUERY: POST_QUERY } = getQuery('allPosts')
const { QUERY: CMPTNPOSTS_QUERY } = getQuery('competitionPosts')
const { QUERY: MYPOSTS_QUERY } = getQuery('myPosts')
const { QUERY: ENTITYPOSTS_QUERY } = getQuery('entityPosts')

function clearPostForm () {
  state.preview = ''
  state.image = null
  state.description = ''
  state.refreshFileUpload++
}

function getCompetitions() {
  if (!state.category || !state.entity) { return }
  state.competition = ''

  const { onResult, onError } = useQuery(gql`
    query competitions ($categoryId: ID!, $entityId: ID!) @connection(key: "competitions", filter: ["categoryId", "entityId"]) {
      competitions (categoryId: $categoryId, entityId: $entityId) {
        globalList {
          name,
          id
        },
        entityList {
          name,
          id
        }
      }
    }
  `,
    {
      categoryId: state.category,
      entityId: state.entity.id
    }
  )

  onResult(({data, loading}) => {
    !loading && (state.competitions = data.competitions)
  })
}

function selectEntity(entityId='1') {
  const entityObj = entity.entities.find(item => item.id == entityId)
  if (entityObj) { state.entity = entityObj }
}

function selectDefault() {
  // Select default entity, category, competition based on the page user is in.
  const { details: {id}, selectedComptn } = categoryInfo
  state.category = id
  state.competition = (!selectedComptn?.expired && selectedComptn?.id) ? selectedComptn.id : ''
  selectEntity(entityInfo.details.id ? entityInfo.details.id : '1')
}

function createNewPost() {

  if (!user.success) {
    auth.open()
    return
  }

  state.alertMsg = ''

  // Check if user part of entity 
  if (state.entity.userAccess == 'NOTFOUND') {
    state.alertMsg = `You're not part of the ${state.entity.name} entity. Join it to post there, or click upload to post in Selfdive entity.`
    selectEntity()
    return
  } else if (state.entity.userAccess == 'PENDING') {
    state.alertMsg = `Your request to join the ${state.entity.name} entity is pending. Please wait for approval before posting.`
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
            ispublic,
            isBot
          },
          coinActivity {
            id,
            points,
            description,
            status,
            createdAt
          },
          entity {
            id,
            stats {
              id,
              posts,
              categories {
                id,
                count
              }
            }
          }
        }
    }

  `, () => ({
      variables: postVariables,
      update: (cache, { data: { createPost } }) => {

        const cacheData: CacheType = {
          category: {
            variables: {category: state.category},
            query: POST_QUERY,
            ignore: !(state.entity.ispublic && createPost.post.ispublic), // Ignore if entity is private and post is not public
            name: 'allPosts'
          },
          entity: {
            variables: {entity: state.entity.id},
            query: ENTITYPOSTS_QUERY,
            name: 'entityPosts',
            ignore: !state.entity.ispublic && state.entity.userAccess != "SUCCESS" // Ignore if enity is private and user don't have access yet
          },
          profile: {
            variables: {},
            query: MYPOSTS_QUERY,
            name: 'myPosts'
          }
        }

        if (state.competition) {
          Object.assign(cacheData, {
            competition: {
              variables: {competition: state.competition, cpType: 'allposts'},
              query: CMPTNPOSTS_QUERY,
              name: 'competitionPosts'
            },
            trending: {
              variables: {competition: state.competition, cpType: 'trending'},
              query: CMPTNPOSTS_QUERY,
              name: 'competitionPosts',
              addEnd: true,
              max: 5
            }
          })

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

        for (let [key, obj] of Object.entries(cacheData)) {

          const { query, variables, name, addEnd, max, ignore } = obj
          const data: AllPostsType | null = cache.readQuery({ query, variables })

          if (data && (!ignore && (!max || data[name].posts.length < max))) {

            const updatedData = updatePosts(name, data, addEnd)
            cache.writeQuery({ query, data: updatedData, variables })

          }
        }

      },
    })
  )

  mutate()

  onDone(() => {
    if (state.entity.userAccess == 'PENDING') {
      toast.$patch({message: "Post uploaded. It'll show in the entity once your part of entity.", color: 'success', open: true})
    } else {
      toast.$patch({message: 'Success! Your post has been uploaded.', color: 'success', open: true})
    }
    state.creatingPost = false
    clearPostForm()
    emit('postCreated')
    const routeToPath = state.entity.ispublic ? `/interests/${state.category}/posts` : `/entity/${state.entity.id}/posts`
    routeToPath != router.path && ionRouter.push(routeToPath)
  })

  onError((error: any) => {
    state.creatingPost = false
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else if (error?.graphQLErrors?.length) {
      toast.$patch({message: error.graphQLErrors[0].message, color: 'primary', open: true})
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
    selectDefault()
    getCompetitions()
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
    max-height: calc(100vh - 370px);
  }
}
</style>

<style lang="scss">
.select-option-header {
  background-color: var(--ion-color-medium-shade);
  font-size: 15px;
  --min-height: 30px !important;
  ion-radio {
    min-height: 30px !important;
    height: 30px;
  }
}
</style>