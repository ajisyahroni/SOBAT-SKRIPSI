import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/classified-page',
    name: 'ClassifiedPage',
    component: () => import('../views/ClassifiedPage.vue')
  },
  {
    path: '/summary-page',
    name: 'SummaryPage',
    component: () => import('../views/SummaryPage.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
