import store from '@/vuex'

interface tokenObject {
    token: string,
    refreshToken: string,
    payload?: {
        username: string
    },
    user?: {
        username: string
    }
}

function storeTokens (response: tokenObject, type: string) {
    // Store the tokens in the local storage and user object in vuex
    const {token, refreshToken, payload, user} = response
    localStorage.setItem('fyptoken', token)
    localStorage.setItem('fyprefreshtoken', refreshToken)
    store.commit('storeUser', {token, refreshToken, username: user ? user.username : payload?.username, success: true })
}

export { storeTokens }