import { reactive, computed, ref, nextTick, onMounted } from "vue"
import { isValidPhoneEmail, isValidEmail, isValidPhone } from "@/utils/validations"
import { getAuth, signOut, RecaptchaVerifier } from "firebase/auth";
import { useAuthStore } from "@/stores/auth";
import { useApolloClient } from '@vue/apollo-composable';

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

function useRecaptchaVerifier () {
    const firebaseAuth = getAuth()
    const auth = useAuthStore()
    onMounted(() => {
        auth.recaptchaVerifier = new RecaptchaVerifier(firebaseAuth, 'recaptcha-verifier', {
            'size': 'invisible',
            'callback': (response: any) => {
                // reCAPTCHA solved, allow signInWithPhoneNumber.
                console.log(response, 'captcha verifcation')
            },
            'expired-callback': () => {
                // Response expired. Ask user to solve reCAPTCHA again.
                console.log('expired')
            }
        })
    }) 
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
        return isValidEmail(fields.emailphone) ? {email: fields.emailphone} : {phone: '+91' + fields.emailphone}
    }

    const emailphoneref = ref()

    function focusEmailPhone() {
        nextTick(() => {
            setTimeout(() => {
                emailphoneref.value.$el.setFocus()
            },)
        })
    }

    function clearPasswords() {
        fields.password1 = ''
        fields.password2 = ''
    }

    const { resolveClient } = useApolloClient()
    const client = resolveClient()

    function resetClientStore() {
        client.resetStore()
    }

    function firebaseSignOut() {
        signOut(getAuth()).then(() => {
          // Sign-out successful.
        }).catch((error) => {
          // An error happened.
        })
    }

    return {
        touched,
        fields,
        valid,
        error,
        getEmailOrPhone,
        clearPasswords,
        focusEmailPhone,
        emailphoneref,
        firebaseSignOut,
        resetClientStore
    }
}

export {
    storeTokens,
    useAuth,
    useRecaptchaVerifier
}