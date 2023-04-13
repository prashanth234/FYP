import { createRouter, createWebHistory } from '@ionic/vue-router'
import { RouteRecordRaw } from 'vue-router'
import TabsPage from '../views/TabsPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'

import MainPage from '../views/MainPage.vue'
import CategoriesPage from '../views/CategoriesPage.vue'
import CategoriesDetailsPage from '../views/CategoryDetailsPage.vue'
import CompetitionDetailsPage from '../views/CompetitionDetailsPage.vue'

import store from '../vuex';


const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/',
    component: MainPage,
    meta: {
      auth: false
    },
    children: [
      {
        path: '/',
        component: CategoriesPage
      },
      {
        path: '/category/:id',
        name: 'CategoryDetails',
        component: CategoriesDetailsPage,
        props: true 
      },
      {
        path: '/competition/:id',
        name: 'CompetitionDetails',
        component: CompetitionDetailsPage,
        props: true 
      },
    ]
  },
  {
    path: '/tabs/',
    component: TabsPage,
    meta: {
      auth: false
    },
    children: [
      {
        path: '',
        redirect: '/tabs/tab1'
      },
      {
        path: 'tab1',
        component: () => import('@/views/Tab1Page.vue')
      },
      {
        path: 'tab2',
        component: () => import('@/views/Tab2Page.vue')
      },
      {
        path: 'tab3',
        component: () => import('@/views/Tab3Page.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.auth && !store.state.user.success) {
    // Redirect the user to the login page if they are not authenticated
    next('/')
  } else {
    // Allow the user to access the route
    next()
  }
});

export default router