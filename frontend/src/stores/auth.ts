import { defineStore } from 'pinia'
import { isValidPhoneEmail, isValidEmail, isValidPhone } from "@/utils/validations"
import { getAuth, signInWithPhoneNumber } from "firebase/auth"

// Used for login, register, forgot passwords and otp forms.

export const useAuthStore = defineStore('auth', {
  state: () => ({ 
    processing: false,
    errors: [] as string[],
    previousForm: '',
    form: '',
    show: false,
    success: false,
    message: "",
    msgType: '',
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
    showMessage(message: string, type: string) {
      this.$patch({message, msgType: type})
    },
    discardMessage() {
      this.message = ''
    },
    changeForm(to: string, postVerify: any = null) {
      this.previousForm = this.form
      this.$patch({
        form: to,
        errors: []
      })
      if (['login', 'register'].includes(to)) {
        this.fields.emailphone = ''
        this.fields.username = ''
        this.fields.otp = ''
        this.clearPasswords()
      } else if (to == 'changepassword') {
        this.clearPasswords()
      }
      this.postVerify = postVerify
    },
    goPreviousForm() {
      if (this.previousForm == 'changepassword') {
        this.form = 'login'
        this.clearPasswords()
      } else {
        this.form = this.previousForm
      }
      this.previousForm = ''
      this.errors = []
    },
    isValidEmailPhone() {
      const valid = isValidPhoneEmail(this.fields.emailphone)
      !valid && (this.errors = ['Please enter valid email or 10 digit IN number'])
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