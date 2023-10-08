<template>

  <ion-page>

    <ion-split-pane content-id="main">

      <ion-menu content-id="main" menu-id="menu">
        <ion-content class="ion-padding">

          <ion-card style="border-radius: 30px;" color="light">
            <ion-card-content style="height: 250px;">
              <ion-row
                v-if="!state.loading"
                class="ion-justify-content-center ion-align-items-center full-height"
                style="align-content: center;"
              >
                <ion-col size="auto">
                  <ion-avatar style="width: 85px;height: 85px;">
                    <img
                      alt="person"
                      :src="userAvatar"
                    />
                  </ion-avatar>
                </ion-col>
                <ion-col size="12" class="ion-text-center" style="padding-top: 20px">
                  <div v-if="user.success">
                    <p style="font-size: 15px"> Welcome Back </p>
                    <p style="font-size: 20px; font-weight: 600;"> {{ user?.username }} </p>
                  </div>
                  <div v-else>
                    <p style="font-size: 15px; font-weight: 600;"> Welcome User </p>
                    <ion-button
                      class="ion-hide-lg-down"
                      @click="openAuth()"
                    >
                      Login
                    </ion-button>
                  </div>
                </ion-col>
              </ion-row>
            </ion-card-content>
          </ion-card>

          <ion-list style="margin-top: 30px">
            <ion-item
              :class="{'ion-item-highlight': router.name == 'home'}"
              lines="none"
              button
              :detail="false"
              @click="navigate('/')"
            >
              <ion-icon
                class="ion-icon-custom cpointer"
                :icon="homeOutline"
              ></ion-icon>
              <ion-label class="list-label">
                Home
              </ion-label>
            </ion-item>
            <ion-item
              :class="{'ion-item-highlight': router.name == 'rewards'}"
              lines="none"
              button
              :detail="false"
              @click="navigate('/rewards')"
              v-if="isUserLogged"
            >
              <ion-icon
                class="ion-icon-custom cpointer"
                :icon="sparklesOutline"
              ></ion-icon>
              <ion-label class="list-label">
                Rewards
              </ion-label>
            </ion-item>
            <ion-item
              :class="{'ion-item-highlight': router.name == 'profile'}"
              lines="none"
              button
              :detail="false"
              @click="navigate('/profile')"
              v-if="isUserLogged"
            >
              <ion-icon
                class="ion-icon-custom cpointer"
                :icon="personOutline"
              ></ion-icon>
              <ion-label class="list-label">
                Profile
              </ion-label>
            </ion-item>
            <ion-item
              lines="none"
              :detail="false"
              button
              @click="logout()"
              v-if="isUserLogged"
            >
              <ion-icon
                class="ion-icon-custom cpointer"
                :icon="logOutOutline"
              ></ion-icon>
              <ion-label class="list-label">
                logout
              </ion-label>
            </ion-item>
          </ion-list>
          
        </ion-content>
      </ion-menu>

      <div class="ion-page" id="main">

        <ion-header>
          <ion-toolbar class="toolbar-nav">
            <ion-buttons slot="start">
              <ion-menu-button></ion-menu-button>
            </ion-buttons>
            <ion-title>
              TBD
            </ion-title>
            <ion-buttons slot="end" v-if="isUserLogged">
              <!-- ion-hide-lg-down  -->
              <ion-button class="ion-padding-end" color="primary" shape="round" fill="outline" @click="postDialog.open">
                <!-- <ion-icon slot="start" :icon="addOutline"></ion-icon> -->
                Add New Post
              </ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>

        <ion-content class="ion-padding">
          <ion-loading v-if="state.loading" :isOpen="state.loading" message="Loading"></ion-loading>
          <ion-router-outlet v-if="!state.loading"></ion-router-outlet>
        </ion-content>

        <ion-footer class="ion-hide-lg-up">
          <ion-tab-bar slot="bottom">
            <ion-tab-button tab="home" :selected="router.name == 'home'" href="/home">
              <ion-icon :icon="homefull" class="tab-bar-icon"/>
              <ion-label>Home</ion-label>
            </ion-tab-button>

            <!-- <ion-tab-button tab="create" v-if="isUserLogged" @click="postDialog.open">
              <ion-icon :icon="addCircle" class="tab-bar-icon"/>
              <ion-label>Create Post</ion-label>
            </ion-tab-button> -->

            <ion-tab-button tab="rewards" href="/rewards" v-if="isUserLogged">
              <ion-icon :icon="sparkles" class="tab-bar-icon" />
              <ion-label>Rewards</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="profile" href="/profile" v-if="isUserLogged">
              <ion-icon :icon="person" class="tab-bar-icon" />
              <ion-label>Profile</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="login" v-if="!isUserLogged">
              <ion-icon :icon="logIn" class="tab-bar-icon" @click="openAuth()" />
              <ion-label>Login</ion-label>
            </ion-tab-button>
          </ion-tab-bar>
        </ion-footer>

      </div>

    </ion-split-pane>

    <ion-modal
      class="login-modal"
      :show-backdrop="true"
      :backdropDismiss="false"
      :is-open="user.auth"
      @didDismiss="closeAuth"
    >
      <ion-button @click="closeAuth" :disabled="state.disableAuthClose" class="close-login" fill="clear">
        <ion-icon size="large" :icon="closeOutline"></ion-icon>
      </ion-button>
      <login-container style="margin-top: 20px;" />
    </ion-modal>

    <ion-modal
      class="create-post-modal"
      :is-open="postDialog.state.isOpen"
      :show-backdrop="true"
      :backdropDismiss="false"
      @willDismiss="postDialog.close"
    >
      <create-post
        :fixed-preview-height="true"
        :showHeader="true"
        @close="postDialog.close"
        @postCreated="postDialog.postCreated"
        type="create"
      />
    </ion-modal>

  </ion-page>

</template>

<script setup lang="ts">
import { menuController, IonTabButton, IonTabBar, IonFooter, IonImg, IonLoading, IonList, IonItem, IonLabel, IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow,  IonMenu, IonSplitPane, IonButtons, IonMenuButton, IonCard, IonCardContent, IonAvatar, useIonRouter } from '@ionic/vue';
import { logOutOutline, closeOutline, homeOutline, personOutline, addCircle, home as homefull, person, logIn, sparklesOutline, sparkles, addOutline } from 'ionicons/icons'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens } from '@/mixims/auth'
import LoginContainer from '@/components/LoginContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { reactive, computed, ref, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { usePostDialog } from '@/composables/postDialog'
import { useApolloClient } from '@vue/apollo-composable'

const { resolveClient } = useApolloClient()
const client = resolveClient()


const ionRouter = useIonRouter();
const router = useRoute();
const user = useUserStore();
const postDialog = usePostDialog();
const toast = useToastStore();

const userAvatar = computed(() => {
  return user?.avatar ? `/media/${user.avatar}?temp=${user.userUpdated}` : '/static/core/avatar.svg'
})

const state = reactive({
  loading: true,
  disableAuthClose: false
})

const isUserLogged = computed(() => {
  return !state.loading && user.success
})

provide('auth', {
  isAuthProcessing,
  authSuccess,
  authFailure
})

function isAuthProcessing(value: boolean) {
  state.disableAuthClose = value
}

function authSuccess(type: string) {
  isAuthProcessing(false)
  type == 'login' && client.resetStore()
}

function authFailure(type: string) {
  isAuthProcessing(false)
}

const closeMenu = async () => {
  // close the menu by menu-id
  await menuController.enable(true, 'menu');
  await menuController.close('menu');
}

function navigate(path: string) {
  closeMenu()
  ionRouter.push(path)
}

function closeAuth() {
  user.$patch({auth: false, authMessage: ''})
}

function openAuth() {
  user.auth = true
}

function checkAuthStatus() {
  if (user.success) { 
    state.loading = false
    return 
  }

  const token = localStorage.getItem('fyptoken')

  if (token) {

    // Verify if the token is vaild or not
    const { mutate, onDone } = useMutation(gql`
      mutation verifyToken ($token: String!) {
          verifyToken (
            token: $token
          ) {
            success,
            errors,
            payload
          }
        }
      `,
      {
        variables: {
          token
        },
        fetchPolicy: "no-cache"
      }
    )

    mutate()

    onDone(({data: {verifyToken}}) => {
      const refreshToken = localStorage.getItem('fyprefreshtoken')

      if (verifyToken.success) {
        user.$patch({success: true})
        state.loading = false
        user.getDetails()
      } else {
        // If not vaild, refresh the token
        logout(false)

        const { mutate, onDone } = useMutation(gql`
          mutation ($refreshToken: String!) {
              refreshToken (
                refreshToken: $refreshToken
              ) {
                success,
                errors,
                payload,
                token,
                refreshToken
              }
            }
          `,
          {
            variables: {
              refreshToken
            },
            fetchPolicy: "no-cache"
          }
        )

        mutate()

        onDone(({data: {refreshToken}}) => {
          if (refreshToken.success) {
            storeTokens(refreshToken, 'refresh')
            user.getDetails()
          }
          state.loading = false
        })
      }
    })
  } else {
    state.loading = false
  }
}

function logout(showToast: boolean = true) {
  navigate('/')
  user.reset()
  client.resetStore()
  showToast && toast.$patch({message: "You've been gracefully logged out. We're looking forward to seeing you login again!", color: 'success', open: true})
}

checkAuthStatus()

</script>

<style scoped lang="scss">
  .close-login {
    position: absolute;
    right: 0px;
    top: 0px;
    color: var(--ion-color-medium);
    cursor: pointer;
    --padding-start: 0px;
    --padding-end: 0px;
  }
  ion-toolbar {
    --min-height: 45px;
  }
  ion-split-pane {
    --side-width: 150px;
    --side-max-width: 150px;
  }
  ion-item {
    height: 55px;
  }
  .ion-item-highlight {
    --background: var(--ion-color-light);
    // --color: var(--ion-color-light);

    &::part(native) {
      border-left: 5px solid var(--ion-color-primary);
    }
  }
  .list-label {
    font-weight: 600;
    padding-left: 12px;
  }
  ion-header {
    -webkit-box-shadow: none;
    box-shadow: none;
    position: initial;
  }
  .toolbar-nav {
  }
  .login-modal {
    --max-width: 100%;
  }
  @media only screen and (min-width: 576px) {
    // For sm and above screens
    .login-modal {
      --height: auto;
      --max-width: 350px;
    }
    .create-post-modal {
      --max-width: 600px !important;
      --height: auto;
    }
  }
  .create-post-modal {
    --max-width: 90%;

    &::part(content) {
      background: none;
      box-shadow: none;
    }
  }
  .tab-bar-icon {
    font-size: 25px;
  }
</style>