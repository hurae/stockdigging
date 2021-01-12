<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('dapan')">
        <div class="card-panel-icon-wrapper icon-dapan">
          <!-- <svg-icon icon-class="peoples" class-name="card-panel-icon" /> -->
          <h2>大盘指数行情</h2>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            今日大盘指数
          </div>
          <count-to :start-val="0" :end-val="3071.11" :duration="300" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('hangqing')">
        <div class="card-panel-icon-wrapper icon-hangye">
          <!-- <svg-icon icon-class="message" class-name="card-panel-icon" /> -->
          <h2>行业指数行情</h2>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            今日行业指数
          </div>
          <count-to :start-val="0" :end-val="2807.92" :duration="300" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('gegu')">
        <div class="card-panel-icon-wrapper icon-gegu">
          <!-- <svg-icon icon-class="message" class-name="card-panel-icon" /> -->
          <h2>单只股票行情</h2>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            今日个股
          </div>
          <count-to :start-val="0" :end-val="2877.92" :duration="300" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from 'vue-count-to'

export default {
  components: {
    CountTo
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-dapan {
        background: #40c9c6;
      }

      .icon-hangye {
        background: #36a3f7;
      }

      .icon-gegu {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-dapan {
      color: #40c9c6;
    }

    .icon-hangye {
      color: #36a3f7;
    }

    .icon-gegu {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
