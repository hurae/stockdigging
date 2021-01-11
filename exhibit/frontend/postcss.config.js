// 给postcss用的
// postcss是帮我们后处理css,
// css已经编译完成了,
// 在stylus-loader编译成css之后,
// 在通过postcss优化css,通过一系列组件去优化,
// 比如以下,通过autoprefixer添加css前缀

module.exports = {
  plugins: {
    autoprefixer: {}
  }
}
