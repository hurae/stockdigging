<script>
export default {
  created() {
    // 路由传参，params对应的是name，query对应的是path
    const { params, query } = this.$route
    const { path } = params
    this.$router.replace({ path: '/' + path, query })
  },
  render: function(h) {
    return h() // avoid warning message
  }
}
</script>
