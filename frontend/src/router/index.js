import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from "@/views/RegisterView.vue";
import AccountView from "@/views/AccountView.vue";


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
      authRequired: true,
    },
  ]
})

// Требование авторизации
router.beforeEach((to, from) => {
  // ...
  // explicitly return false to cancel the navigation
  if (to.name !== 'login' && !isAuthenticated) this.$router.push({ name: 'login'});
  else return true
})


export default router
