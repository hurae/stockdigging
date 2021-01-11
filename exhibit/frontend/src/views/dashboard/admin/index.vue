<template>
  <div class="dashboard-editor-container">
    <panel-group @handleSetLineChartData="handleSetLineChartData" />
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px">
      <line-chart :chart-data="lineChartData" />
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'

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
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    LineChart
  },
  data() {
    return {
      lineChartData: lineChartData.dapan
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
