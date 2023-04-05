import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import TabsPage from '../views/TabsPage.vue';
import LoginPage from '../views/LoginPage.vue';

// import CategoryMainPage from '../views/CategoriesPage.vue'
import CategoriesPage from '../views/CategoriesPage.vue';
import CategoriesDetailsPage from '../views/CategoryDetailsPage.vue';

import store from '../vuex';


const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/category',
    component: CategoriesPage
  },
  {
    path: '/category/:id',
    name: 'CategoryDetails',
    component: CategoriesDetailsPage
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
        component: CategoriesPage
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

// router.beforeEach((to, from, next) => {
//   if (to.meta.auth && !store.state.user.success) {
//     // Redirect the user to the login page if they are not authenticated
//     next('/');
//   } else {
//     // Allow the user to access the route
//     next();
//   }
// });

export default router