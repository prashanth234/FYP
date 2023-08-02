<template>

  <button  @click="emitfromchild">click me</button>

  <input type="file" name="fileUpload" accept="image/*" @change="emitfromchild" />

</template>

<script lang="ts" setup>
  defineProps({
    firstName: String,
    lastName: String,
    modelValue: String
  })

  const emit = defineEmits(['update:firstName', 'update:lastName', 'update:modelValue'])

  function emitfromchild () {
    emit('update:firstName', 'prashanth')
    emit('update:lastName', 'Bodduna')
    emit('update:modelValue', 'test')
  }
</script>