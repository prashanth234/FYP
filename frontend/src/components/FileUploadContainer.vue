<template>
  <div id="file-upload-form" class="uploader">

    <input id="file-upload" @change="handleFileUpload" type="file" name="fileUpload" accept="image/*" />

    <label for="file-upload" id="file-drag">

      <ion-img style="height: 200px" :src="previewImage" v-if="previewImage"></ion-img>

      <div id="start">
        <div v-if="!previewImage">
          <ion-icon :icon="cloudUploadOutline" size="large"></ion-icon>
        </div>
        <ion-button size="small" color="primary">{{ previewImage ? 'Change Image' : 'Select Image' }}</ion-button>
      </div>

    </label>

  </div>
</template>

<script setup lang="ts">
import { cloudUploadOutline } from 'ionicons/icons'
import { ref } from 'vue'

defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const imageUrl = ref('');
const previewImage = ref('');

function handleFileUpload({target: { validity, files: [file],},}) {
  if (validity.valid) {
    imageUrl.value = file
    emit('update:modelValue', file);
    if (file) {
      const reader = new FileReader();

      reader.onload = () => {
        previewImage.value = reader.result;
      };

      reader.readAsDataURL(file);
    }
  }
}

</script>

<style>
.uploader {
  display: block;
  clear: both;
  width: 100%;
}
.uploader label {
  float: left;
  clear: both;
  width: 100%;
  padding: 20px;
  text-align: center;
  background: #fff;
  border-radius: 4px;
  border: 2px solid #dddfe2;
  transition: all 0.2s ease;
  cursor: pointer;
}
.uploader label:hover {
  border-color: #3880ff;
}
.uploader label.hover {
  border: 3px solid #3880ff;
  box-shadow: inset 0 0 0 6px #eee;
}
.uploader label.hover #start i.fa {
  transform: scale(0.8);
  opacity: 0.3;
}
.uploader #start {
  float: left;
  clear: both;
  width: 100%;
  margin-top: 20px;
}
.uploader #start.hidden {
  display: none;
}
.uploader #start i.fa {
  font-size: 50px;
  margin-bottom: 1rem;
  transition: all 0.2s ease-in-out;
}
.uploader input[type=file] {
  display: none;
}
.uploader div {
  margin: 0 0 0.5rem 0;
  color: #5f6982;
}
</style>