// 设置title为路由title，如果不是的话就默认title
import defaultSettings from '@/settings'

const title = defaultSettings.title || 'Stock Analyses'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
