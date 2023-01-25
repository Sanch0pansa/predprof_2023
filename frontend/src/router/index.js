import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from "@/views/RegisterView.vue";
import AccountView from "@/views/account/AccountView.vue";
import VerifyTelegramView from "@/views/Account/VerifyTelegramView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
      meta: {
        authRequired: true,
      },
    },
    {
      path: '/account/verify_telegram',
      name: 'verify_telegram',
      component: VerifyTelegramView,
      meta: {
        authRequired: true,
      },
    },
  ]
})

export default router
