import { defineStore } from 'pinia'
import { isValidPhoneEmail, isValidEmail, isValidPhone } from "@/utils/validations"
import { getAuth, signInWithPhoneNumber } from "firebase/auth"

export const useAuthStore = defineStore('auth', {
  state: () => ({ 
    processing: false,
    errors: [] as string[],
    form: '',
    show: false,
    success: false,
    message: '',
    postVerify: null as any,
    recaptchaVerifier: null as any,
    otpVerifier: null as any,
    fields: {
      emailphone: '',
      username: '',
      password1: '',
      password2: '',
      otp: ''
    }
  }),
  getters: {
    emailOrPhone(): {email?: string, phone?: string} {
      const emailphone = this.fields.emailphone
      return isValidEmail(emailphone) ? 
      { email: emailphone } : 
      { phone: `+91${emailphone}` }
    },
    isInputPhone(): boolean {
      return isValidPhone(this.fields.emailphone)
    },
  },
  actions: {
    open() {
      this.form = 'login'
      this.show = true
    },
    close() {
      this.$reset()
    },
    processState(value: boolean) {
      this.processing = value
      value && (this.errors = [])
    },
    discardMessage() {
      this.message = ''
    },
    changeForm(to: string, postVerify: any = null) {
      this.$patch({
        form: to,
        errors: []
      })
      if (['login', 'register'].includes(to)) {
        this.fields.emailphone = ''
        this.fields.username = ''
        this.fields.otp = ''
        this.clearPasswords()
      } else if (to == 'change-password') {
        this.clearPasswords()
      }
      this.postVerify = postVerify
    },
    isValidEmailPhone() {
      const valid = isValidPhoneEmail(this.fields.emailphone)
      !valid && (this.errors = ['Please enter valid email or phone'])
      return valid
    },
    isValidEmail() {
      const valid = isValidEmail(this.fields.emailphone)
      !valid && (this.errors = ['Please enter valid email'])
      return valid
    },
    clearErrors() {
      this.errors = []
    },
    clearPasswords() {
      this.fields.password1 = ''
      this.fields.password2 = ''
    },
    async sendOTP() {
      const phone = this.emailOrPhone.phone || ''
      if (!phone) { return { success: false } }
      try {
        this.otpVerifier = await signInWithPhoneNumber(getAuth(), phone, this.recaptchaVerifier)
        return { success: true }
      } catch (error) {
        return { success: false, error }
      }
    }
  }
})