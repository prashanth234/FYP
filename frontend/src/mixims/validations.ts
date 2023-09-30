
export function isValidEmail(email) {
    return email.match(
        /^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
    );
}

// export function validate(ev: HTMLIonInputElement, types=['required']) {
//     const value = ev.target.value;

//     event.target.classList.remove('ion-valid');
//     event.target.classList.remove('ion-invalid');

//     const valid = types.every(type => {
//         if (type == 'email') {
//             return isValidEmail(value)
//         } else {
//             return value != ''
//         }
//     });

//     valid
//         ? event.target.classList.add('ion-valid')
//         : event.target.classList.add('ion-invalid');

//     return valid
// }

// export function markTouched(ev) {
//     ev.target.classList.add('ion-touched');
// }