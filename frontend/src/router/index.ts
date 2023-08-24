import { createRouter, createWebHistory } from '@ionic/vue-router'
import { RouteRecordRaw } from 'vue-router'

import MainPage from '@/views/MainPage.vue'
import CategoriesPage from '@/views/CategoriesPage.vue'
import CategoriesDetailsPage from '@/views/CategoryDetailsPage.vue'
import MyProfilePage from '@/views/MyProfilePage.vue'
import ActivatePage from '@/views/activatePage.vue'
import RewardsPage from '@/views/RewardsPage.vue'

import { useUserStore } from '@/stores/user'
import store from '../vuex';

import TempChild from '@/views/TempChild.vue'
import TempPage from '@/views/TempPage.vue'
import TempMain from '@/views/TempMain.vue'



const routes: Array<RouteRecordRaw> = [
  {
    path: '/temp',
    name: 'Temp',
    component: TempPage,
    props: true,
    children: [
      {
        path: '',
        component: TempMain
      },
      {
        path: 'child/:id',
        component: TempChild
      }
    ]
  },
  {
    path: '/activate/:token',
    name: 'Activate',
    component: ActivatePage
  },
  {
    path: '/',
    component: MainPage,
    meta: {
      auth: false
    },
    children: [
      {
        path: '',
        component: CategoriesPage,
        name: 'home'
      },
      {
        path: 'interests/:id',
        name: 'CategoryDetails',
        component: CategoriesDetailsPage,
        props: true
      },
      {
        path: 'profile',
        component: MyProfilePage,
        name: 'profile',
        meta: {
          auth: true
        }
      },
      {
        path: 'rewards',
        component: RewardsPage,
        name: 'rewards',
        meta: {
          auth: true
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const user = useUserStore()

  if (to.meta.auth && !user.success) {
    // Redirect the user to the login page if they are not authenticated
    next('/')
  } else {
    // Allow the user to access the route
    next()
  }
  
});

export default router