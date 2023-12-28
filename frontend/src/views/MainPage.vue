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
                    <div style="font-size: 16px; font-weight: 600;"> Welcome </div>
                    <div class="two-line-ellipsis" style="font-size: 20px; font-weight: 600;"> {{ displayName }} </div>
                  </div>
                  <div v-else>
                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 10px;"> Welcome User </div>
                    <ion-button
                      class="ion-hide-lg-down"
                      @click="auth.open"
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

        <doc-links />
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
              <ion-button class="ion-hide-sm-up add-post-theme add-post-mobile" @click="addNewPost" shape="round">
                <ion-icon :icon="addOutline"></ion-icon>
              </ion-button>
              <ion-button class="ion-hide-sm-down ion-margin-end add-post add-post-theme" shape="round" @click="addNewPost">
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
              @click="item.maction && item.maction()"
            >
              <ion-icon :icon="item.micon" class="tab-bar-icon"/>
              <ion-label>{{ item.name }}</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="login" v-if="!isUserLogged" @click="auth.open">
              <ion-icon :icon="logIn" class="tab-bar-icon" />
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
      :is-open="auth.show"
      @didDismiss="auth.close"
    >
      <ion-progress-bar v-if="auth.processing" type="indeterminate"></ion-progress-bar>
      <ion-button v-else @click="auth.close" :disabled="auth.processing" class="close-login" fill="clear">
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

    <!-- About Modal -->
    <ion-modal
      class="about-modal ion-text-center"
      :is-open="state.aboutDialog"
      :show-backdrop="true"
      :backdropDismiss="false"
      @willDismiss="closeAbout"
    >
      <div class="ion-padding">
        <div>
          About this app
        </div>
        <ion-button
					size="small"
					color="light"
					@click="closeAbout"
				>
					Close
				</ion-button>
      </div>
    </ion-modal>

    <!-- Common Dialog -->
    <common-dialog @action="$event => $event.control()"></common-dialog>

  </ion-page>

</template>

<script setup lang="ts">
import { menuController, IonTabButton, IonTabBar, IonFooter, IonLoading, IonList, IonItem, IonLabel, IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow,  IonMenu, IonSplitPane, IonButtons, IonMenuButton, IonCard, IonCardContent, IonAvatar, useIonRouter, IonProgressBar } from '@ionic/vue';
import { addOutline, logOutOutline, closeOutline, homeOutline, personOutline, home as homefull, person, logIn, sparklesOutline, sparkles, help, helpCircle, information, informationCircle, fastFood } from 'ionicons/icons'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens, useAuth } from '@/composables/auth'
import LoginContainer from '@/components/LoginContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import DocLinks from '@/components/DocLinksContainer.vue'
import { reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { usePostDialog } from '@/composables/postDialog'

import { useDialogStore } from '@/stores/dialog'
import CommonDialog from '@/components/CommonDialogContainer.vue'
import { warningOutline } from 'ionicons/icons'
import { useAuthStore } from '@/stores/auth';


const ionRouter = useIonRouter();
const router = useRoute();
const postDialog = usePostDialog();

const user = useUserStore();
const toast = useToastStore();
const dialog = useDialogStore();
const auth = useAuthStore();
const { resetClientStore } = useAuth();

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
  aboutDialog: false,
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
      auth: true,
      dicon: help,
      micon: helpCircle,
      action: navigate.bind(null, '/support')
    },
    {
      name: 'About',
      auth: false,
      dicon: information,
      micon: informationCircle,
      action: showAbout,
      maction: showAbout
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

function addNewPost () {
  if (!user.success) {
  auth.showMessage('Ready to share your content? Log in and start posting!', 'info')
  auth.open()
  return
  }
  postDialog.open()
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

function showAbout() {
  state.aboutDialog = true
}

function closeAbout() {
  state.aboutDialog = false
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
  resetClientStore()
  showToast && toast.$patch({message: "Logged out. Seen you again soon!", color: 'success', open: true})
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
    // For xs screens
    --max-width: 100%;
    // --height: auto;
  }
  .create-post-modal {
    // For xs screens
    --max-width: 100%;
    
    // &::part(content) {
    //   background: none;
    //   box-shadow: none;
    // }
  }
  .about-modal {
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
    .about-modal {
      --height: auto;
      --max-width: 600px;
    }
  }
  .tab-bar-icon {
    font-size: 25px;
  }
  .add-post-theme {
    --background: linear-gradient(135deg, #54BFFC, #0D51FC);
// --background: linear-gradient(135deg, #3dc2ff, #3880FF);
    // --background: linear-gradient(135deg, #3dc2ff, #0F52BA); (vue colors)

    --color: #ffffff;
  }
  .add-post-mobile {
    --padding-end: 10px;
    --padding-start: 10px;
  }
  .add-post {
    --padding-end: 25px;
    --padding-start: 25px;
    font-size: 15px;
    font-weight: 650;
    margin: 10px;
    margin-right: 20px;
  }
</style>