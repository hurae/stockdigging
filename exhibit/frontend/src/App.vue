<!-- 入口界面-->
<template>
  <div id="app">
    <!-- <router-view> 是用来渲染通过路由映射过来的组件，当路径更改时，<router-view> 中的内容也会发生更改-->
    <router-view />
  </div>
</template>

<script>
// export用于对外输出本模块（一个文件可以理解为一个模块）变量的接口,每个模块仅有一个
// 使用export default命令，为模块指定默认输出，这样就不需要知道所要加载模块的变量名。
export default {
  name: 'App'
}
// App.vue是我们的主组件，所有页面都是在App.vue下进行切换的。
</script>
