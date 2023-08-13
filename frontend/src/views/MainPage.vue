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
          <ion-toolbar>
            <ion-buttons slot="start">
              <ion-menu-button></ion-menu-button>
            </ion-buttons>
            <ion-title>
              TBD
            </ion-title>
            <ion-buttons slot="end" v-if="isUserLogged">
              <ion-button
                @click="onClickPoints"
                class="ion-padding-end"
              >
                <ion-img
                  style="width: 25px; height: 25px; margin-right: 7px;"
                  src="/static/core/coins.png"
                ></ion-img>
                Points
              </ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>

        <ion-content class="ion-padding">
          <ion-loading :isOpen="state.loading" message="Loading"></ion-loading>
          <ion-router-outlet v-if="!state.loading"></ion-router-outlet>
        </ion-content>

      </div>

    </ion-split-pane>

    <ion-modal class="login-modal" :show-backdrop="true" :is-open="user.auth" @didDismiss="closeLogin">
      <ion-icon @click="closeLogin" class="close-login" size="large" :icon="closeOutline"></ion-icon>
      <login-container style="margin-top: 20px;" />
    </ion-modal>

  </ion-page>

  <!-- <ion-page>

    <ion-header class="ion-custom-header">
      <ion-toolbar>
        <ion-grid class="padding-zero padding-col-zero">
          <ion-row class="ion-align-items-center">
            <ion-col>
              <ion-title>TBD</ion-title>
            </ion-col>
            <ion-col size="auto" v-if="user.success">
              <ion-icon class="icon-custom cpointer" :icon="logOutOutline" @click="logout()"></ion-icon>
            </ion-col>
            <ion-col size="auto" class="ion-padding-end" v-else>
              <ion-button @click="login()">Login</ion-button>
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-toolbar>
    </ion-header> 

    <ion-content>
      <ion-modal :show-backdrop="true" :is-open="user.auth" @didDismiss="closeLogin">
        <ion-icon @click="closeLogin" class="close-login" size="large" :icon="closeOutline"></ion-icon>
        <login-container />
      </ion-modal>

      <div slot="fixed" class="side-toolbar">

        <ion-card class="full-height margin-zero">
          <ion-row class="full-height ion-text-center">

            <ion-col size="12">
              <ion-title>TBD</ion-title>
              <ion-icon class="ion-icon-custom cpointer" style="padding-top: 25px" :icon="homeOutline"></ion-icon>
            </ion-col>

            <ion-col size="12" class="ion-align-self-end">
              <ion-icon
                v-if="user.success" class="ion-icon-custom cpointer"
                :icon="logOutOutline" @click="logout()"
              ></ion-icon>
              <ion-button
                v-else fill="clear"
                size="small" @click="login()"
              >
                Login
              </ion-button>
            </ion-col>

          </ion-row>
        </ion-card>

      </div>

      <ion-router-outlet></ion-router-outlet>
      
    </ion-content>
    
  </ion-page> -->
</template>

<script setup lang="ts">
import { IonImg, IonLoading, IonList, IonItem, IonLabel, IonPage, IonButton, IonModal, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow,  IonMenu, IonSplitPane, IonButtons, IonMenuButton, IonCard, IonCardContent, IonAvatar, useIonRouter } from '@ionic/vue';
import { logOutOutline, closeOutline, homeOutline, personOutline, trendingDown } from 'ionicons/icons'
import store from '@/vuex'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { storeTokens } from '@/mixims/auth'
import LoginContainer from '@/components/LoginContainer.vue'
import { reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const ionRouter = useIonRouter();
const router = useRoute();
const user = useUserStore();

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
  // ionRouter.push('/login')
}

function getUserDetails() {
  const { result, onResult } = useQuery(gql`   
                              query {
                                me {
                                  username,
                                  avatar
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
      mutation ($token: String!) {
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
  .login-modal {
    --max-width: 100%;
  }
  @media only screen and (min-width: 576px) {
    // For sm and above screens
    .login-modal {
      --height: auto;
      --max-width: 350px;
    }
  }
  ion-header {
    -webkit-box-shadow: none;
    box-shadow: none;
    position: initial;
  }
  // ion-grid {
  //   --ion-grid-padding: 0px;
  //   padding-top: 5px;
  //   font-size: 25px !important;
  // }
  // ion-modal {
  //   --background: transparent;
  //   --backdrop-opacity: 70%;
  //   --border-radius: 5px;
  //   --box-shadow: 0px;
  //   --height: auto;
  // }
  // .side-toolbar {
  //   top: 20px;
  //   left: 20px;
  //   height: calc(100vh - 40px);
  //   width: 60px;
  // }
  // .ion-custom-header {
  //   position: initial;
  //   padding-top: 15px;
  //   padding-left: 20px;
  //   padding-right: 20px;
  //   border-radius: 5px
  // }
</style>