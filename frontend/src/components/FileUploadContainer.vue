<template>

  <div id="file-upload-form" class="uploader" v-if="!props.simple">

    <input id="file-upload" @change="handleFileUpload" type="file" name="fileUpload" accept="image/*" />

    <label for="file-upload" id="file-drag">

      <ion-img style="height: 200px" :src="state.previewImage" v-if="state.previewImage"></ion-img>

      <div id="start">
        <div v-if="!state.previewImage">
          <ion-icon :icon="cloudUploadOutline" size="large"></ion-icon>
        </div>
        <ion-button size="small" color="primary" style="pointer-events: none">{{ state.previewImage ? 'Change Image' : 'Select Image' }}</ion-button>
      </div>

    </label>

  </div>

  <div class="simple-uploader" v-else>

    <input
      id="file-upload"
      ref="fileupload"
      type="file"
      name="fileUpload"
      accept="image/*"
      @change="$event => props.cropable ? loadImage($event) : handleFileUpload($event)" 
    />

    <slot name="handler" :selectImage="selectImage">
      <ion-button @click="selectImage()" for="file-upload" size="small" color="primary">Select Image</ion-button>
    </slot>

  </div>

  <ion-modal class="crop-modal custom-modal" :is-open="state.openCropper" :show-backdrop="true" @willDismiss="closeCropper">
    <ion-card style="width: 300px">
      <ion-card-content>
        <ion-row>
          <ion-col size="12">
            <cropper
              :stencil-component="CircleStencil"
              :src="state.imageUrl"
              @change="onCropChange"
              ref="cropperRef"
            />
          </ion-col>
          <ion-col size="12">
            <ion-button
              size="small"
              color="danger"
              @click="cropImage"
              style="float: right"
            >
              Done
            </ion-button>
            <ion-button
              size="small"
              @click="closeCropper"
              color="light"
              style="float: right; margin-right: 15px;"
            >
              Cancel
            </ion-button>
          </ion-col>
        </ion-row>
      </ion-card-content>
    </ion-card>
  </ion-modal>

</template>

<script setup lang="ts">
import { IonIcon, IonImg, IonButton, IonModal, IonCard, IonRow, IonCol, IonCardContent } from '@ionic/vue'
import { CircleStencil, Cropper, CropperResult } from 'vue-advanced-cropper'
import { cloudUploadOutline } from 'ionicons/icons'
import { reactive, ref, onUnmounted } from 'vue'
import type { Ref } from 'vue'

const props = defineProps<{
  simple: Boolean,
  modelValue: File | null,
  cropable: Boolean,
  preview?: string | CropperResult
}>()

const emit = defineEmits(['update:modelValue', 'update:preview'])

interface State {
  // Image is blob object
  image: Blob | null,
  // ImageUrl is blob object url
  imageUrl: string,
  imageType: string,
  previewImage: string | CropperResult,
  openCropper: Boolean
}

const state: State = reactive({
  image: null,
  imageUrl: '',
  imageType: '',
  previewImage: '',
  openCropper: false
})

const cropperRef: Ref<any>  = ref(null)
const fileupload: Ref<HTMLElement | null>  = ref(null)

function handleFileUpload(event: Event) {
  const {validity, files} = event.target as HTMLInputElement 
  
  if (validity.valid && files && files.length) {
    state.image = files[0]
    
    emit('update:modelValue', files[0])

    if (files[0]) {
      const reader = new FileReader()

      reader.onload = () => {
        state.previewImage = reader.result as string
        emit('update:preview', state.previewImage)
      };
      reader.readAsDataURL(files[0])
    }
  }
}

function selectImage() {
  fileupload.value?.click()
}

function getMimeType(file: string | ArrayBuffer | null | undefined, fallback = '') {
	const byteArray = (new Uint8Array(file)).subarray(0, 4);

  let header = '';
  
  for (let i = 0; i < byteArray.length; i++) {
      header += byteArray[i].toString(16);
  }

	switch (header) {
    case "89504e47":
        return "image/png";
    case "47494638":
        return "image/gif";
    case "ffd8ffe0":
    case "ffd8ffe1":
    case "ffd8ffe2":
    case "ffd8ffe3":
    case "ffd8ffe8":
        return "image/jpeg";
    default:
        return fallback;
  }
}

function loadImage(event: Event) {
  const { files } = event.target as HTMLInputElement;
  
  if (files && files[0]) {

    // Revoke the object URL, to allow the garbage collector to destroy the uploaded before file
    if (state.imageUrl) {
      URL.revokeObjectURL(state.imageUrl)
    }

    // Create the blob link to the file to optimize performance
    const blob: string = URL.createObjectURL(files[0])
    
    // Create a new FileReader to read this image binary data
    const reader = new FileReader()

    reader.onload = (e) => {
      state.imageUrl = blob
      state.imageType = getMimeType(e.target?.result, files[0].type)
      state.openCropper = true
    }

    // Start the reader job - read file as a data url (base64 format)
    reader.readAsArrayBuffer(files[0])
  }
}

function cropImage() {
  const { canvas } = cropperRef.value?.getResult()

  if (canvas) {
    canvas.toBlob((blob: Blob | null) => {
      state.image = blob
      emit('update:modelValue', blob)
      emit('update:preview', state.previewImage, state.imageType.split('/')[1])
      closeCropper()
    }, state.imageType)
  }
}

function closeCropper(){
  state.openCropper = false
}

function onCropChange(preview: CropperResult) {
  state.previewImage = preview
}

onUnmounted(() => {
  if (state.imageUrl) {
    URL.revokeObjectURL(state.imageUrl)
  }
})
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
.crop-modal {
  --max-width: 600px;
}
</style>