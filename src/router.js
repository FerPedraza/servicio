import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login.vue'
import Principal from './components/Principal.vue'
import Formato from './components/Formato.vue'
import Bandeja from './components/Bandeja.vue'
import Datos from './components/Datos.vue'
import adminUsers from './components/adminUsers.vue'
import firebase from 'firebase'
import BandejaSalida from './components/BandejaSalida.vue'
import VModal from 'vue-js-modal'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'

Vue.use(VueMaterial)
 
Vue.use(VModal)

Vue.use(Router)

let router=new Router({
  mode:"history",
  routes: [
    {
      path: '*',
      redirect: '/login'
    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/principal',
      name: 'principal',
      component: Principal,
      meta: {
        requiresAuth: false
      },
      children:[
        {
          path:'formato',
          name:'formato',
          component:Formato
        },
        {
          path:'bandeja',
          name:'bandeja',
          component:Bandeja
        },
        {
          path:'bandejasalida',
          name:'bandejasalida',
          component:BandejaSalida
        },
        {
          path:'datos',
          name:'datos',
          component:Datos
        },
        {
          path:'adminusers',
          name:'adminusers',
          component:adminUsers
        }
      ]
    }
  ]
})
router.beforeEach((to, from, next) => {
  let currentUser = firebase.auth().currentUser;
  let requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !currentUser) next('login')
  else if (!requiresAuth && currentUser) next('principal')
  else next()
})
export default router
