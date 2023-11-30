import { getAuth, RecaptchaVerifier, signInWithPhoneNumber, signOut, onAuthStateChanged } from "firebase/auth";
import { ref, onMounted, reactive } from 'vue';

function useAuthVerify() {
  const auth = getAuth()
  const cnfmResult = ref()
  const recaptchaVerifier = ref()
  
  const status = reactive({
    sendingOtp: false,
    verifyingOtp: false
  })
  
  onAuthStateChanged(auth, (usr) => {
    if (usr) {
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/auth.user
      console.log(usr)
      // ...
    } else {
      // User is signed out
      console.log("singed out")
    }
  });

  onMounted(() => {
    
    recaptchaVerifier.value = new RecaptchaVerifier(auth, 'recaptcha-verifier', {
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

  async function sendOTP(phone: string) {
    status.sendingOtp = true
    try {
      const confirmationResult = await signInWithPhoneNumber(auth, phone, recaptchaVerifier.value)
      cnfmResult.value = confirmationResult
      status.sendingOtp = false
      return { success: true }
    } catch (error) {
      status.sendingOtp = false
      return { success: false, error }
    }
  }

  async function verifyOTP(otp: string) {
    status.verifyingOtp = true
    try {
      const response = await cnfmResult.value.confirm(otp)
      status.verifyingOtp = false
      return { success: true, user: response.user }
    } catch (error) {
      status.verifyingOtp = false
      return { success: false, error }
    }
  }

  function firebaseSignOut() {
    signOut(auth).then(() => {
      // Sign-out successful.
    }).catch((error) => {
      // An error happened.
    });
  }

  return {
    status,
    cnfmResult,
    sendOTP,
    verifyOTP,
    firebaseSignOut
  }
}

export {
  useAuthVerify
}