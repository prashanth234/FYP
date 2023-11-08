<template>

  <ion-page>

    <ion-split-pane content-id="main">

      <!-- Side Menu-->
      <ion-menu content-id="main" menu-id="menu">
        <ion-content class="ion-padding">

          <!-- Avatar card-->
          <ion-card style="border-radius: 30px;">
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
                <ion-col size="12" class="ion-text-center" style="padding-top: 20px; color: var(--ion-color-dark)">
                  <div v-if="user.success">
                    <div style="font-size: 15px; font-weight: 600;"> Welcome </div>
                    <div style="font-size: 20px; font-weight: 600;"> {{ displayName }} </div>
                  </div>
                  <div v-else>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 10px;"> Welcome User </div>
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

          <!-- Navigation list in menu -->
          <ion-list style="margin-top: 40px">
            <ion-item
              v-for="(item, index) in state.navigations"
              :key="index"
              :class="{'ion-item-highlight': router.name == item.rname}"
              lines="none"
              button
              :detail="false"
              @click="item.action"
              v-show="!item.auth || isUserLogged"
            >
              <ion-icon
                class="ion-icon-custom cpointer"
                :icon="item.dicon"
              ></ion-icon>
              <ion-label class="list-label">
                {{ item.name }}
              </ion-label>
            </ion-item>
          </ion-list>
          
        </ion-content>
      </ion-menu>

      <!-- Content Page -->
      <div class="ion-page" id="main">

        <ion-header>
          <ion-toolbar class="toolbar-nav">
            <ion-buttons slot="start">
              <ion-menu-button></ion-menu-button>
            </ion-buttons>
            <ion-title>
              TBD
            </ion-title>
            <ion-buttons slot="end">
              <!-- ion-hide-lg-down  -->
              <ion-button class="ion-padding-end" color="primary" shape="round" fill="outline" @click="addNewPost">
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

            <ion-tab-button
              v-for="(item, index) in state.navigations"
              :key="index"
              :tab="item.rname"
              :selected="router.name == item.rname"
              :href="item.rpath"
              v-show="item.micon && (!item.auth || isUserLogged)"
            >
              <ion-icon :icon="item.micon" class="tab-bar-icon"/>
              <ion-label>{{ item.name }}</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="login" v-if="!isUserLogged">
              <ion-icon :icon="logIn" class="tab-bar-icon" @click="openAuth()" />
              <ion-label>Login</ion-label>
            </ion-tab-button>

          </ion-tab-bar>
        </ion-footer>

      </div>

    </ion-split-pane>

    <!-- Login Model -->
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

    <!-- Create Post Model-->
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

    <!-- Common Dialog -->
    <common-dialog @action="$event => $event.control()"></common-dialog>

  </ion-page>

</template>

<script setup lang="ts">
import { menuController, IonTabButton, IonTabBar, IonFooter, IonLoading, IonList, IonItem, IonLabel, IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow,  IonMenu, IonSplitPane, IonButtons, IonMenuButton, IonCard, IonCardContent, IonAvatar, useIonRouter } from '@ionic/vue';
import { logOutOutline, closeOutline, homeOutline, personOutline, home as homefull, person, logIn, sparklesOutline, sparkles, helpCircleOutline, helpCircle } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens } from '@/composables/auth'
import LoginContainer from '@/components/LoginContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { reactive, computed, ref, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { usePostDialog } from '@/composables/postDialog'
import { useApolloClient } from '@vue/apollo-composable'

import { useDialogStore } from '@/stores/dialog'
import CommonDialog from '@/components/commonDialogContainer.vue'
import { warningOutline } from 'ionicons/icons'

const { resolveClient } = useApolloClient()
const client = resolveClient()


const ionRouter = useIonRouter();
const router = useRoute();
const user = useUserStore();
const postDialog = usePostDialog();
const toast = useToastStore();
const dialog = useDialogStore();

const userAvatar = computed(() => {
  return user?.avatar ? `/media/${user.avatar}` : '/static/core/avatar.svg'
})

const displayName = computed(() => {
  if (user) {
    if (user.firstName || user.lastName) {
      return `${user.firstName} ${user.lastName}`
    } else {
      return user.username
    }
  }
  return ''
})

const state = reactive({
  loading: true,
  disableAuthClose: false,
  navigations: [
    {
      name: 'Home',
      rname: 'home',
      rpath: '/home',
      auth: false,
      dicon: homeOutline,
      micon: homefull,
      action: navigate.bind(null, '/')
    },
    {
      name: 'Rewards',
      rname: 'rewards',
      rpath: '/rewards',
      auth: true,
      dicon: sparklesOutline,
      micon: sparkles,
      action: navigate.bind(null, '/rewards')
    },
    {
      name: 'Profile',
      rname: 'profile',
      rpath: '/profile',
      auth: true,
      dicon: personOutline,
      micon: person,
      action: navigate.bind(null, '/profile')
    },
    {
      name: 'Support',
      rname: 'support',
      rpath: '/support',
      auth: false,
      dicon: helpCircleOutline,
      micon: helpCircle,
      action: navigate.bind(null, '/support')
    },
    {
      name: 'Logout',
      auth: true,
      rpath: '',
      dicon: logOutOutline,
      action: confirmLogout
    }
  ]
})

const isUserLogged = computed(() => {
  return !state.loading && user.success
})

provide('auth', {
  isAuthProcessing,
  authSuccess,
  authFailure
})

function addNewPost () {
  if (!user.success) {
    user.authMessage = 'Ready to share your content? Log in and start posting!'
    user.auth = true
    return
  }
  postDialog.open()
}

function isAuthProcessing(value: boolean) {
  state.disableAuthClose = value
}

function authSuccess(type: string) {
  isAuthProcessing(false)
  client.resetStore()
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

function confirmLogout() {
  const buttons = [
    {title: 'Yes', color: 'primary', action: 'logout', control: logout},
    {title: 'Cancel', color: 'light'}
  ]

  dialog.show(
    'Are you sure you want to log out?',
    '',
    buttons,
    warningOutline,
    'warning'
  )
}

function logout(showToast: boolean = true) {
  navigate('/')
  user.reset()
  client.resetStore()
  showToast && toast.$patch({message: "See you again soon! You've been logged out gracefully.", color: 'success', open: true})
  dialog.open = false
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
    --min-height: 40px;
    margin: 8px 0px 8px 0px; 
    --background: transparent;
  }
  ion-list {
    border-radius: 10px;
    padding: 0px
  }
  .ion-item-highlight {
    --background: var(--ion-color-light);

    &::part(native) {
      border-left: 5px solid var(--ion-color-primary);
    }
  }
  .list-label {
    font-weight: 550;
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