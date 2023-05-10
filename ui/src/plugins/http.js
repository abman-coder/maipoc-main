import axios from 'axios'
import configs from '../config'
import cacheHandler from './cache.interceptor'

const axiosCall = async (method, url, body, noloading, hds = {}) => {
    let response = null;
    let cacheResponse = cacheHandler.get(method, url, body)
    if (cacheResponse) return cacheResponse

    let config = {
        headers: { "Authorization": `Bearer ${localStorage.token}`, ...hds }
    }
    let Loader = document.getElementById('loader')

    if (!noloading) {
        if (Loader) Loader.style.display = "block"
    }
    try {
        response = await axios[method](configs.apiUrl + url, body || config, config)
    } catch (err) {
        response = err.response || {}
    } finally {
        if (Loader) Loader.style.display = "none"
        if (response?.data && response?.data.code === 401) {
            if (response?.data.description === "Unable to parse authentication token.") {
                // if (!localStorage.token) return {}
                const trail = +(localStorage.trail || 0)
                if (!trail || trail < 3) {
                    localStorage.trail = trail + 1;
                    await new Promise(resolve => setTimeout(resolve, 700))
                    return axiosCall(method, url, body, noloading, hds)
                }
                if (localStorage.token) return { data: { code: 401 } }
            } else {
            }
            if (window.location.pathname !== "/") {
                localStorage.previousPath = window.location.pathname
                window.location.href = window.location.origin
            } else {
                return {}
            }
        }
        localStorage.trail = 0

        cacheHandler.put(method, url, body, response)
        return response;
    }
}

export const methods = {
    post: (url, data, noloading = false) => axiosCall("post", url, data, noloading),
    put: (url, data, noloading = false) => axiosCall("put", url, data, noloading),
    get: (url, noloading = false) => axiosCall("get", url, null, noloading),
    remove: (url, noloading = false, hds = {}) => axiosCall("delete", url, null, noloading, hds),
}
