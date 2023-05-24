<template>

  <div id="file-upload-form" class="uploader" v-if="!props.simple">

    <input id="file-upload" @change="handleFileUpload" type="file" name="fileUpload" accept="image/*" />

    <label for="file-upload" id="file-drag">

      <ion-img style="height: 200px" :src="previewImage" v-if="previewImage"></ion-img>

      <div id="start">
        <div v-if="!previewImage">
          <ion-icon :icon="cloudUploadOutline" size="large"></ion-icon>
        </div>
        <ion-button size="small" color="primary" style="pointer-events: none">{{ previewImage ? 'Change Image' : 'Select Image' }}</ion-button>
      </div>

    </label>

  </div>

  <div class="simple-uploader" v-else>

    <ion-img style="height: 200px" :src="previewImage" v-if="previewImage"></ion-img>
    <input id="file-upload" type="file" name="fileUpload" accept="image/*" @change="handleFileUpload" />

    <ion-row class="padding-col-zero">
      <ion-col size="auto">
        <ion-button @click="selectImage()" for="file-upload" size="small" color="primary">{{ previewImage ? 'Change Image' : 'Select Image' }}</ion-button>
      </ion-col>
      <ion-col>
        <slot name="right-slot"></slot>
      </ion-col>
    </ion-row>

  </div>

</template>

<script setup lang="ts">
import { IonIcon, IonImg, IonButton, IonCol, IonRow } from '@ionic/vue';
import { cloudUploadOutline, image } from 'ionicons/icons'
import { ref } from 'vue'
import type { Ref } from 'vue'

const props = defineProps(['modelValue', 'simple'])
const emit = defineEmits(['update:modelValue'])

const imageUrl: Ref<File|undefined> = ref();
const previewImage: Ref<string> = ref(props.modelValue || '');

function handleFileUpload(event: Event) {
  const {validity, files} = event.target as HTMLInputElement 
  
  if (validity.valid && files && files.length) {
    imageUrl.value = files[0]
    
    emit('update:modelValue', files[0]);

    if (files[0]) {
      const reader = new FileReader();

      reader.onload = () => {
        previewImage.value = reader.result as string;
      };

      reader.readAsDataURL(files[0]);
    }
  }
}

function selectImage() {
  document.getElementById('file-upload')?.click()
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
  border-color: var(--ion-color-primary);
}
.uploader label.hover {
  border: 3px solid var(--ion-color-primary);
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
#file-upload {
  display: none;
}
</style>