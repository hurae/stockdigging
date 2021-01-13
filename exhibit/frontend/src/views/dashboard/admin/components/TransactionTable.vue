<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column 
      label="股票名称" 
      width="100" 
      prop="stockname" 
      @col-click="more">
    </el-table-column>
    <el-table-column label="预测涨跌幅" width="100" align="center" prop="percent">
    </el-table-column>
  </el-table>
</template>

<script>
import { transactionList } from '@/api/remote-search'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    }
  },
  data() {
    return {
      list: [
        {
          stockname:'12345',
          percent:'21231'
        }
      ]
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {

      transactionList().then(response => {
        this.list = response.data.items.slice(0, 8)
      })
    },
    more() {
      this.$router.push({path:'/register'})
    }
}}
</script>

