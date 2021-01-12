<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="股票名称" min-width="100">
      <template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column>
    <el-table-column label="股票代码" width="200" align="center">
      <template slot-scope="scope">
        {{ scope.row.price | toThousandFilter }}
      </template>
    </el-table-column>
    <el-table-column label="上市公司" width="200" align="center">
      <template slot-scope="scope">
        {{ scope.row.price | toThousandFilter }}
      </template>
    </el-table-column>
    <el-table-column label="预测涨跌幅" width="200" align="center">
      <template slot-scope="scope">
        {{ scope.row.price | toThousandFilter }}
      </template>
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
      list: null
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
    }
  }
}
</script>
