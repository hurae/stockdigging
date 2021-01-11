// utils:全局公用方法
import Cookies from 'js-cookie'

const TokenKey = 'stockAnalyses-Token'

// 获取token
export function getToken() {
  return Cookies.get(TokenKey)
}

// 设置token
export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

// 移除token
export function removeToken() {
  return Cookies.remove(TokenKey)
}
