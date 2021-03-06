import Vue from 'vue'

import Cookies from 'js-cookie'

import 'normalize.css/normalize.css' // a modern alternative to CSS resets

import Element from 'element-ui'
import './styles/element-variables.scss'
// import enLang from 'element-ui/lib/locale/lang/en'// 如果使用中文语言包请默认支持，无需额外引入，请删除该依赖

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import './icons' // icon
import './permission' // permission control
import './utils/error-log' // error log

import * as filters from './filters' // global filters

if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}

Vue.use(Element, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
  // locale: enLang// 如果使用中文，无需设置，请删除
})

Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

// main.js作为项目的入口文件，在main.js中，新建了一个Vue实例
new Vue({
  // 告诉该实例要挂载的地方；（即实例装载到index.html中的位置）
  el: '#app',
  router,
  store,
  // render: h => h(App) 是下面内容的缩写：
  // render: function (createElement) {
  //   return createElement(App);
  // }
  // h是 Vue.js 里面的createElement函数，
  // 这个函数的作用就是生成一个 VNode节点，
  // render 函数得到这个VNode 节点之后，
  // 返回给 Vue.js的mount函数，渲染成真实DOM节点，并挂载到根节点上
  render: h => h(App)
})
