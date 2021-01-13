<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">

        <el-col :span="6" :xs="24">
          <user-card :user="user" />
        </el-col>

        <el-col :span="18" :xs="24">
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="大盘指数" name="dapan">
                <line-chart :chart-data="lineChartData" />
              </el-tab-pane>
              <el-tab-pane label="行业指数" name="hangqing">
                <line-chart :chart-data="lineChartData" />
              </el-tab-pane>
              <el-tab-pane label="个股详情" name="gegu">
                <line-chart :chart-data="lineChartData" />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>

      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import UserCard from './components/UserCard'
import LineChart from '../dashboard/admin/components/LineChart'

const lineChartData = {
  dapan: {
    openData: [1000, 120, 1610, 1340, 1050, 600, 1650],
    closeData: [1200, 820, 910, 540, 1620, 1400, 1450]
    // highData: [100, 1200, 610, 340, 650, 160, 450],
    // lowData: [200, 890, 910, 940, 620, 1400, 450]
  },
  hangqing: {
    openData: [2000, 1920, 1200, 1440, 600, 1300, 1400],
    closeData: [800, 1600, 510, 1060, 1405, 1500, 1300]
    // highData: [1000, 1200, 1610, 1340, 1050, 1600, 1650],
    // lowData: [500, 820, 910, 740, 1620, 1400, 1450]
  },
  gegu: {
    openData: [200, 920, 1200, 1440, 600, 300, 1400],
    closeData: [800, 600, 910, 1560, 405, 1500, 300]
    // highData: [1000, 1200, 610, 740, 1050, 600, 650],
    // lowData: [900, 720, 510, 1540, 620, 1400, 650]
  }
}

export default {
  name: 'Profile',
  components: { UserCard, LineChart },
  data() {
    return {
      user: {},
      activeTab: 'dapan'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ])
  },
  created() {
    this.getUser()
  },
  methods: {
    getUser() {
      this.user = {
        name: this.name,
        role: this.roles.join(' | '),
        email: 'admin@test.com',
        avatar: this.avatar
      }
    }
  }
}
</script>
