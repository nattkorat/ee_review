import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProjectView from '../views/ProjectView.vue'
import TaskView from '@/views/TaskView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/projects/:id',
      name: 'project',
      component: ProjectView,
    },
    {
      path: '/projects/:projectId/tasks/:taskId',
      name: 'task',
      component: TaskView,
    }
  ],
})

export default router
