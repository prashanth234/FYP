import { reactive, computed } from "vue"
import { isValidPhoneEmail, isValidEmail, isValidPhone } from "@/mixims/validations"
import { fileTray } from "ionicons/icons"

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
    const { token, refreshToken } = response
    localStorage.setItem('fyptoken', token)
    localStorage.setItem('fyprefreshtoken', refreshToken)
}

function useAuth() {
    const touched = reactive({
        emailphone: false,
        email: false,
        phone: false
    })

    const fields = reactive({
        emailphone: '',
        username: '',
        password1: '',
        password2: '',
        email: '',
        firstName: '',
        lastName: '',
        dob: '',
        gender: '',
        phone: ''
    })

    const valid = computed(() => {
        return {
            emailphone: isValidPhoneEmail(fields.emailphone),
            email: isValidEmail(fields.email),
            phone: isValidPhone(fields.phone)
        }
    })

    // It is usefull for inputs to show error after field is touched
    const error = computed(() => {
        return {
            emailphone: touched.emailphone && !valid.value.emailphone,
            email: touched.email && !valid.value.email,
            phone: touched.phone && !valid.value.phone
        }
    })
    
    function getEmailOrPhone() {
        return isValidEmail(fields.emailphone) ? {email: fields.emailphone} : {phone: fields.emailphone}
    }

    return {
        touched,
        fields,
        valid,
        error,
        getEmailOrPhone
    }
}

export { storeTokens, useAuth }