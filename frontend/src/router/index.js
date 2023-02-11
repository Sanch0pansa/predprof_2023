import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from "@/views/RegisterView.vue";
import AccountView from "@/views/account/AccountView.vue";
import VerifyTelegramView from "@/views/Account/VerifyTelegramView.vue";
import SinglePageView from "@/views/SinglePageView.vue";
import CreatePageView from "@/views/CreatePageView.vue";
import ModerationView from "@/views/Moderation/ModerationView.vue";
import ModerationPagesView from "@/views/Moderation/ModerationPagesView.vue";
import ModerationReviewsView from "@/views/Moderation/ModerationReviewsView.vue";
import ModerationReportsView from "@/views/Moderation/ModerationReportsView.vue";
import AdminView from "@/views/Admin/AdminView.vue";


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
        authUpdate: true,
      },
    },
    {
      path: '/account/verify_telegram',
      name: 'verify_telegram',
      component: VerifyTelegramView,
      meta: {
        authRequired: true,
        authUpdate: true,
      },
    },
    {
      path: '/page/:id',
      name: 'single_page',
      component: SinglePageView,
    },
    {
      path: '/create_page',
      name: 'create_page',
      component: CreatePageView,
      meta: {
        authRequired: true,
        authUpdate: true,
      },
    },
    {
      path: '/moderation/',
      name: 'moderation',
      component: ModerationView,
      meta: {
        authRequired: true,
        authUpdate: true,
        moderatorRequired: true,
      },
    },
    {
      path: '/moderation/pages/',
      name: 'moderation_pages',
      component: ModerationPagesView,
      meta: {
        authRequired: true,
        authUpdate: true,
        moderatorRequired: true,
      },
    },
    {
      path: '/moderation/reviews/',
      name: 'moderation_reviews',
      component: ModerationReviewsView,
      meta: {
        authRequired: true,
        authUpdate: true,
        moderatorRequired: true,
      },
    },
    {
      path: '/moderation/reports/',
      name: 'moderation_reports',
      component: ModerationReportsView,
      meta: {
        authRequired: true,
        authUpdate: true,
        moderatorRequired: true,
      },
    },
    {
      path: '/admin/',
      name: 'admin',
      component: AdminView,
      meta: {
        authRequired: true,
        authUpdate: true,
        moderatorRequired: true,
        adminRequired: true,
      },
    },
  ]
})

export default router
