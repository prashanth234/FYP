// import { InputCustomEvent } from '@ionic/vue';

export function isValidEmail(email: string) {
    const pat = /^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
    return pat.test(email)
}

export function isValidPhone(phone: string) {
    const pat = /^[6-9]\d{9}$/
    return pat.test(phone)
}

export function isValidPhoneEmail(input: string) {
    return isValidPhone(input) || isValidEmail(input)
}

// export function validate(event: InputCustomEvent, types=['required']) {
//     const value = event.target.value

//     event.target.classList.remove('ion-valid')
//     event.target.classList.remove('ion-invalid')

//     const valid = types.every(type => {
//         if (!value) {return false}
//         const input = value.toString()
//         if (type == 'email') {
//             return isValidEmail(input)
//         } else if (type == 'phoneemail') {
//             return isValidPhoneEmail(input)
//         } else {
//             return input != ''
//         }
//     });

//     valid
//         ? event.target.classList.add('ion-valid')
//         : event.target.classList.add('ion-invalid')

//     return valid
// }

// export function markTouched(ev: InputCustomEvent) {
//     ev.target.classList.add('ion-touched')
// }