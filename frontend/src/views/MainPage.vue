<template>

  <ion-page>

    <ion-split-pane content-id="main">

      <ion-menu content-id="main">
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
                  <ion-button
                    v-else
                    @click="login()"
                  >
                    Login
                  </ion-button>
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
              @click="home()"
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
              :class="{'ion-item-highlight': router.name == 'profile'}"
              lines="none"
              button
              :detail="false"
              @click="profile()"
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
              <ion-button class="ion-hide-lg-down ion-padding-end" color="primary" fill="outline" @click="postDialog.open">
                Create New Post
              </ion-button>
              <ion-button
                @click="onClickPoints"
                class="ion-padding-end"
                fill="outline"
              >
                <ion-img
                  style="width: 25px; height: 25px;"
                  src="/static/core/coins.png"
                ></ion-img>
                <span class="ion-hide-lg-down" style="margin-left: 7px;">Rewards</span>
              </ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>

        <ion-content class="ion-padding">
          <ion-loading :isOpen="state.loading" message="Loading"></ion-loading>
          <ion-router-outlet v-if="!state.loading"></ion-router-outlet>
        </ion-content>

        <ion-footer class="ion-hide-lg-up" >
          <ion-tab-bar slot="bottom">
            <ion-tab-button tab="" href="/home">
              <ion-icon :icon="homefull" class="tab-bar-icon"/>
              <ion-label>Home</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="create" v-if="isUserLogged">
              <ion-icon :icon="addCircle" @click="postDialog.open" class="tab-bar-icon"/>
              <ion-label>Create Post</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="profile" href="/profile" v-if="isUserLogged">
              <ion-icon :icon="person" class="tab-bar-icon" />
              <ion-label>Profile</ion-label>
            </ion-tab-button>

            <ion-tab-button tab="login" v-if="!isUserLogged">
              <ion-icon :icon="logIn" class="tab-bar-icon" @click="login()" />
              <ion-label>Login</ion-label>
            </ion-tab-button>
          </ion-tab-bar>
        </ion-footer>

      </div>

    </ion-split-pane>

    <ion-modal class="login-modal" :show-backdrop="true" :is-open="user.auth" @didDismiss="closeLogin">
      <ion-icon @click="closeLogin" class="close-login" size="large" :icon="closeOutline"></ion-icon>
      <login-container style="margin-top: 20px;" />
    </ion-modal>

    <ion-modal
      class="create-post-modal"
      :is-open="postDialog.state.isOpen"
      :show-backdrop="true"
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
import { IonTabButton, IonTabBar, IonFooter, IonImg, IonLoading, IonList, IonItem, IonLabel, IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow,  IonMenu, IonSplitPane, IonButtons, IonMenuButton, IonCard, IonCardContent, IonAvatar, useIonRouter } from '@ionic/vue';
import { logOutOutline, closeOutline, homeOutline, personOutline, addCircle, home as homefull, person, logIn } from 'ionicons/icons'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens } from '@/mixims/auth'
import LoginContainer from '@/components/LoginContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { usePostDialog } from '@/composables/postDialog'


const ionRouter = useIonRouter();
const router = useRoute();
const user = useUserStore();
const postDialog = usePostDialog();

const userAvatar = computed(() => {
  return user?.avatar ? `/media/${user.avatar}?temp=${user.userUpdated}` : '/static/core/avatar.svg'
})

const state = reactive({
  loading: true
})

const isUserLogged = computed(() => {
  return !state.loading && user.success
})

function onClickPoints() {
  ionRouter.push('/rewards')
}

function logout() {
  localStorage.removeItem('fyptoken')
  localStorage.removeItem('fyprefreshtoken')
  user.$reset()
}

function home() {
  ionRouter.push('/')
}

function profile() {
  ionRouter.push('/profile')
}

function closeLogin() {
  user.auth = false
}

function login() {
  user.auth = true
}

function getUserDetails() {
  const { result, onResult } = useQuery(gql`   
                              query me {
                                me {
                                  username,
                                  firstName,
                                  lastName,
                                  email,
                                  gender,
                                  avatar,
                                  points
                                }
                              }
                            `)
  
  onResult(({data, loading}) => {
    if (loading) return
    if (data.me) {
      user.$patch({...data.me, userUpdated: user.userUpdated + 1})
    } else {
      logout()
    }
  })
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
        }
      }
    )

    mutate()

    onDone(({data: {verifyToken}}) => {
      const refreshToken = localStorage.getItem('fyprefreshtoken')

      if (verifyToken.success) {
        user.$patch({success: true})
        state.loading = false
        getUserDetails()
      } else {
        // If not vaild, refresh the token
        logout()
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
            }
          }
        )

        mutate()

        onDone(({data: {refreshToken}}) => {
          if (refreshToken.success) {
            storeTokens(refreshToken, 'refresh')
            getUserDetails()
          }
          state.loading = false
        })
      }
    })
  } else {
    state.loading = false
  }
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
      --max-width: 600px;
    }
  }
  .create-post-modal {
    --max-width: 90%;
    --height: auto;

    &::part(content) {
      background: none;
      box-shadow: none;
    }
  }
  .tab-bar-icon {
    font-size: 25px;
  }
</style>