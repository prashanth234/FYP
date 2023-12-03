<template>
  <input
    type="number"
    class="digit-box"
    v-for="(el, ind) in digits"
    :autofocus="ind == 0"
    :key="ind"
    v-model="digits[ind]"
    :maxlength="1"
    @keyup="handleKeyDown($event, ind)"
    ref="otpCont"
  />
</template>
 
 <script lang="ts" setup>
  import { onMounted, reactive, ref } from 'vue';

  const props = defineProps({
    digitCount: {
      type: Number,
      required: true
    },
    modelValue: String
  })

  const digits: string[] = reactive([])
  const otpCont = ref<HTMLInputElement[]>([])
  const emit = defineEmits(['update:modelValue'])

  onMounted(() => {
    setTimeout(() => {
      otpCont.value[0].focus()
    }, 100);
  })

  for (let i =0; i < props.digitCount; i++) {
    digits[i] = ''
  }

  const handleKeyDown = async function (event: any, index: number) {

    if (event.key !== "Tab" && 
        event.key !== "ArrowRight" &&
        event.key !== "ArrowLeft"
    ) {
      event.preventDefault();
    }
    
    if (event.key === "Backspace") {
      if (index != 0 && digits[index] == '') {
        otpCont.value[index-1].focus()
      }

      digits[index] = ''
      updateModel()
      return
    }

    if ((new RegExp('^([0-9])$')).test(event.key)) {
      digits[index] = event.key

      if (index != props.digitCount - 1) {
        otpCont.value[index+1].focus()
      }
    } else if (event.key == 'ArrowRight') {
      if (index != props.digitCount - 1) {
        otpCont.value[index+1].focus()
      }
    } else if (event.key == 'ArrowLeft') {
      if (index != 0) {
        otpCont.value[index-1].focus()
      }
    }

    updateModel()
  }

  function updateModel() {
    emit('update:modelValue', digits.toString().replaceAll(',', ''))
  }


</script>

<style scoped>
.digit-box {
  height: 30px;
  width: 30px;
  border: 1px solid var(--ion-color-step-300, #b3b3b3);
  display: inline-block;
  border-radius: 5px;
  margin: 5px;
  /* padding: 15px; */
  font-size: 1rem;
  text-align: center;
}

.digit-box:focus {
  border: 2px solid var(--ion-color-primary);
}
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
  -moz-appearance:textfield;
}
</style>