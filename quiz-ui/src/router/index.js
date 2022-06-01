import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NotFoundPage from '../components/NotFoundPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: () => import('../views/Quiz/NewQuizPage.vue')
    },
    {
      path: '/questions',
      name: 'questions',
      component: () => import('../views/Quiz/QuestionsManager.vue')
    },
    {
      path: '/score',
      name: 'score',
      component: () => import('../views/Quiz/ScoreView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Admin/LoginView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/Admin/AdminView.vue')
    },
    {
      path: '/admin/question/create',
      name: 'admin-question-create',
      component: () => import('../views/Admin/CreateQuestionView.vue')
    },
    {
      path: '/admin/question/watch/:position',
      name: 'admin-question-watch',
      component: () => import('../views/Admin/WatchQuestionView.vue')
    },
    {
      path: '/admin/question/edit/:position',
      name: 'admin-question-edit',
      component: () => import('../views/Admin/EditQuestionView.vue')
    },
    {
      path: '/error',
      name: 'error',
      component: () => import('../views/ErrorView.vue')
    },
    { path: '/:pathMatch(.*)*', component: NotFoundPage }
  ]
})

export default router
