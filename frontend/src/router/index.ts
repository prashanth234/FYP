import { createRouter, createWebHistory } from '@ionic/vue-router'
import { RouteRecordRaw } from 'vue-router'

import MainPage from '@/views/MainPage.vue'
import CategoriesPage from '@/views/CategoriesPage.vue'
import CategoriesDetailsPage from '@/views/CategoryDetailsPage.vue'
// import MyProfilePage from '@/views/MyProfilePage.vue'
// import ActivatePage from '@/views/ActivatePage.vue'
// import RewardsPage from '@/views/RewardsPage.vue'
// import SupportPage from '@/views/SupportPage.vue'
// import PasswordResetPage from '@/views/PasswordResetPage.vue'
// import PrivacyPage from '@/views/PrivacyPage.vue'
// import TermsPage from '@/views/TermsPage.vue'


import { useUserStore } from '@/stores/user'

// import TempChild from '@/views/TempChild.vue'
// import TempPage from '@/views/TempPage.vue'
// import TempMain from '@/views/TempMain.vue'

const routes: Array<RouteRecordRaw> = [
  // {
  //   path: '/temp',
  //     name: 'Temp',
  //     component: TempPage,
  //     props: true,
  //     children: [
  //         {
  //       path: '',
  //             component: TempMain
  //         },
  //         {
  //       path: 'child/:id',
  //             component: TempChild
  //         }
  //   ]
  // },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('@/views/PrivacyPage.vue')
  },
  {
    path: '/terms',
    name: 'Terms',
    component: () => import('@/views/TermsPage.vue')
  },
  {
    path: '/activate/:token',
    name: 'Activate',
    component: () => import('@/views/ActivatePage.vue')
  },
  {
    path: '/password-reset/:token',
    name: 'PasswordReset',
    component: () => import('@/views/PasswordResetPage.vue')
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
        path: 'interests/:id/posts/:postid?',
        name: 'CategoryDetails',
        component: CategoriesDetailsPage,
        props: true
      },
      {
        path: 'entity',
        component: () => import('@/views/EntityPage.vue'),
        name: 'entity'
      },
      {
        path: 'entity/create',
        component: () => import('@/views/CreateEntityPage.vue'),
        name: 'createEntity',
        meta: {
          auth: true
        }
      },
      {
        path: 'entity/:editId',
        component: () => import('@/views/CreateEntityPage.vue'),
        name: 'editEntity',
        props: true,
        meta: {
          auth: true
        }
      },
      {
        path: 'entity/:id/posts/:postid?',
        component: () => import('@/views/EntityDetailsPage.vue'),
        name: 'EntityDetails',
        props: true
      },
      {
        path: 'profile',
        component: () => import('@/views/MyProfilePage.vue'),
        name: 'profile',
        meta: {
          auth: true
        }
      },
      {
        path: 'rewards',
        component: () => import('@/views/RewardsPage.vue'),
        name: 'rewards',
        meta: {
          auth: true
        }
      },
      {
        path: 'support',
        component: () => import('@/views/SupportPage.vue'),
        name: 'support',
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