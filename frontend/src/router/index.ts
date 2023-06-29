import { createRouter, createWebHistory } from '@ionic/vue-router'
import { RouteRecordRaw } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'

import MainPage from '../views/MainPage.vue'
import CategoriesPage from '../views/CategoriesPage.vue'
import CategoriesDetailsPage from '../views/CategoryDetailsPage.vue'
import MyProfilePage from '@/views/MyProfilePage.vue'
import LoginFormContianer from '@/components/LoginFormContainer.vue'
import TempPage from '@/views/TempPage.vue'

import store from '../vuex';


const routes: Array<RouteRecordRaw> = [
  {
    path: '/temp',
    name: 'Temp',
    component: TempPage
  },
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
        path: '/profile',
        component: MyProfilePage,
        meta: {
          auth: true
        }
      },
    ]
  },
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