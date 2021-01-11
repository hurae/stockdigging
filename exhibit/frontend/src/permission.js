// permission management
import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

// NProgress是页面跳转是出现在浏览器顶部的进度条
NProgress.configure({ showSpinner: false }) // NProgress Configuration
// 禁用进度环

const whiteList = ['/login', '/auth-redirect', '/'] // no redirect whitelist
// 全局路由守卫
// async的用法，它作为一个关键字放到函数前面,
// 用于表示函数是一个异步函数，因为async就是异步的意思，
// 异步函数也就意味着该函数的执行不会阻塞后面代码的执行，
// async函数返回的是一个promise对象。
// Promise对象代表了未来将要发生的事件，用来传递异步操作的消息。
router.beforeEach(async(to, from, next) => {
  // to,要去的路由
  // from,当前的路由
  // next，放行

  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/login') {
      // if is logged in, redirect to the home page
      next({ path: '/' })
      NProgress.done() // hack: https://github.com/PanJiaChen/vue-element-admin/pull/2939
    } else {
      // determine whether the user has obtained his permission roles through getInfo
      const hasRoles = store.getters.roles && store.getters.roles.length > 0
      if (hasRoles) {
        // 1、next()：进行管道中的下一个钩子。如果全部钩子执行完了，则导航的状态就是confirmed（确认的）。
        // 2、next(false)：中断当前的导航。如果浏览器的URL改变了（可能是用户手动或者浏览器后退按钮），那么URL地址会重置到from路由对应的地址。
        // 3、next（'/'）或者next({path:'/'}):跳转到一个不同的地址。当前的导航被中断，然后进行一个新的导航。你可以向next传递任意位置对象，且允许设置诸如replace：true、name:'home'之类的选项以及任何用在router-link的toProp或router.push中的选项。
        // 4、next(error)如果传入next的参数是一个Error实例，则导航会被终止且该错误会被传递给router.onError()注册过的回调。
        next()
      } else {
        try {
          // get user info
          // note: roles must be a object array! such as: ['admin'] or ,['developer','editor']

          // await的含义为等待。意思就是代码需要等待await后面的函数运行完并且有了返回结果之后，才继续执行下面的代码
          const { roles } = await store.dispatch('user/getInfo') // ?

          // generate accessible routes map based on roles
          const accessRoutes = await store.dispatch('permission/generateRoutes', roles) // ?

          // dynamically add accessible routes
          router.addRoutes(accessRoutes)

          // hack method to ensure that addRoutes is complete
          // set the replace: true, so the navigation will not leave a history record
          next({ ...to, replace: true })
          // 使用next({ ...to, replace: true })来确保addRoutes()时动态添加的路由已经被完全加载上去。
          // next({ ...to, replace: true })中的replace: true只是一个设置信息，告诉VUE本次操作后，不能通过浏览器后退按钮，返回前一个路由。
          // 因此next({ ...to, replace: true })可以写成next({ ...to })，不过你应该不希望用户在addRoutes()还没有完成的时候，可以点击浏览器回退按钮搞事情吧。
          // 其实next({ ...to })的执行很简单，它会判断：
          // 如果参数to不能找到对应的路由的话，就再执行一次beforeEach((to, from, next)直到其中的next({ ...to})能找到对应的路由为止。
          // 也就是说此时addRoutes()已经完成啦，找到对应的路由之后，接下来将执行前往对应路由的beforeEach((to, from, next) ，因此需要用代码来判断这一次是否就是前往对应路由的beforeEach((to, from, next)，如果是，就执行next()放行。
          // 如果守卫中没有正确的放行出口的话，会一直next({ ...to})进入死循环 !!!
          // 因此你还需要确保在当addRoutes()已经完成时，所执行到的这一次beforeEach((to, from, next)中有一个正确的next()方向出口。
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          Message.error(error || 'Has Error')
          next(`/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token*/

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

// beforeEach是路由跳转前执行的，afterEach是路由跳转后执行的。
router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
