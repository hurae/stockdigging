// Babel 有两种并行的配置文件格式，可以一起使用，也可以分开使用。
// 项目范围的配置
// babel.config.js 文件，具有不同的拓展名（json、js、html）
// babel.config.js 是按照 commonjs 导出对象，可以写js的逻辑。
// 相对文件的配置
// .babelrc 文件，具有不同的拓展名
// 总结：baberc 的加载规则是按目录加载的，是只针对自己的代码。
// config的配置针对了第三方的组件和自己的代码内容。
// babel.config.js 是一个项目级别的配置，一般有了babel.config.js 就不会在去执行.babelrc的设置。

module.exports = {
  presets: [
    // https://github.com/vuejs/vue-cli/tree/master/packages/@vue/babel-preset-app
    '@vue/cli-plugin-babel/preset'
  ],
  'env': {
    'development': {
      // babel-plugin-dynamic-import-node plugin only does one thing by converting all import() to require().
      // This plugin can significantly increase the speed of hot updates, when you have a large number of pages.
      // https://panjiachen.github.io/vue-element-admin-site/guide/advanced/lazy-loading.html
      'plugins': ['dynamic-import-node']
    }
  }
}
