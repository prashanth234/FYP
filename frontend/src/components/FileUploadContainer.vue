<template>

  <div class="simple-uploader" v-if="props.simple">

    <input
      id="file-upload"
      ref="fileupload"
      type="file"
      name="fileUpload"
      :accept="props.fileType || 'image/*'"
      @input="$event => props.cropable ? loadImage($event) : reduceImageSize($event)" 
    />

    <slot name="handler" :selectImage="selectImage" :loading="state.processingImage">
      <ion-button @click="selectImage()" for="file-upload" size="small" color="primary">Select Image</ion-button>
    </slot>

  </div>

  <div id="file-upload-form" class="uploader" v-else>

    <input id="file-upload" @change="handleFileUpload" type="file" name="fileUpload" :accept="props.fileType || 'image/*'" />

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

  <ion-modal class="crop-modal" :is-open="state.openCropper" :show-backdrop="true" @willDismiss="closeCropper">

    <ion-row class="ion-padding ion-justify-content-center" v-if="state.cropperLoading">
      <ion-spinner 
        class="button-loading-small"
        name="crescent"
      />
    </ion-row>

    <ion-row class="ion-padding">
      <ion-col size="12">
        <cropper
          :stencil-component="CircleStencil"
          :src="state.imageUrl"
          :canvas="{width: 600, height: 600}"
          @change="onCropChange"
          @ready="state.cropperLoading=false"
          ref="cropperRef"
        />
      </ion-col>
      <ion-col size="12">
        <ion-button
          size="small"
          color="primary"
          @click="cropImage"
          :disabled="state.cropperLoading"
          class="float-right"
        >
          Done
        </ion-button>
        <ion-button
          size="small"
          @click="closeCropper"
          color="light"
          class="float-right"
          style="margin-right: 15px;"
        >
          Cancel
        </ion-button>
      </ion-col>
    </ion-row>
  </ion-modal>

</template>

<script setup lang="ts">
import { IonIcon, IonImg, IonButton, IonModal, IonRow, IonCol, IonSpinner } from '@ionic/vue'
import { CircleStencil, Cropper, CropperResult } from 'vue-advanced-cropper'
import { cloudUploadOutline } from 'ionicons/icons'
import { reactive, ref, onUnmounted } from 'vue'
import type { Ref } from 'vue'

const props = defineProps<{
  simple: Boolean,
  modelValue: File | null,
  cropable: Boolean,
  preview?: string | CropperResult,
  fileType?: string
}>()

const emit = defineEmits(['update:modelValue', 'update:preview'])

interface State {
  // Image is blob object
  image: Blob | null,
  // ImageUrl is blob object url
  imageUrl: string,
  imageType: string,
  previewImage: string,
  cropperPreview: CropperResult | null,
  openCropper: boolean,
  processingImage: boolean,
  cropperLoading: boolean
}

const state: State = reactive({
  image: null,
  imageUrl: '',
  imageType: '',
  previewImage: '',
  cropperPreview: null,
  openCropper: false,
  processingImage: false,
  cropperLoading: false
})

const cropperRef: Ref<any>  = ref(null)
const fileupload: Ref<HTMLInputElement | null>  = ref(null)

// Without cropper directly update the model and preview by reducing size
function reduceImageSize(event: Event) {
  const {validity, files} = event.target as HTMLInputElement;

  if (validity.valid && files && files.length) {
    const file = files[0]
    const reader = new FileReader()
    state.processingImage = true

    reader.onload = function (e) {
      const img = new Image()
      img.src = e.target?.result as string

      img.onload = function () {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')
        const maxWidth = 2048 // Adjust this to your desired maximum width
        const maxHeight = 1620 // Adjust this to your desired maximum height
        let width = img.width
        let height = img.height

        if (width > maxWidth || height > maxHeight) {
          if (width / maxWidth > height / maxHeight) {
            width = maxWidth
            height = (img.height / img.width) * maxWidth
          } else {
            height = maxHeight;
            width = (img.width / img.height) * maxHeight
          }
        }

        canvas.width = width
        canvas.height = height

        // file.type to get original file type
        const fileType = 'image/jpeg'

        ctx?.drawImage(img, 0, 0, width, height)

        function handleBlob(blob: Blob | null) {
          if (blob) {
            const resizedFile = new File([blob], file.name, { type: fileType });
            state.image = resizedFile
            emit('update:modelValue', resizedFile)
          }
          state.processingImage = false
        }

        // You can convert the canvas content back to an image or upload the canvas data directly
        // For example, convert to a blob and upload using FormData:
        canvas.toBlob(handleBlob, fileType);

        // Display the resized image in the preview element
        state.previewImage = canvas.toDataURL(fileType)
        emit('update:preview', state.previewImage)
      }
    }

    reader.readAsDataURL(file)
  }
}

// Without cropper directly update the model and preview
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

function getMimeType(file: any, fallback = '') {
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

// Setting up things for the cropper
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
      // state.imageType = getMimeType(e.target?.result, files[0].type)
      state.imageType = 'image/jpeg'
      state.openCropper = true
      state.cropperLoading = true
    }

    // Start the reader job - read file as a data url (base64 format)
    reader.readAsArrayBuffer(files[0])
  }
}

// After the image is cropped
function cropImage() {
  const { canvas } = cropperRef.value?.getResult()

  if (canvas) {
    canvas.toBlob((blob: Blob | null) => {
      state.image = blob
      emit('update:modelValue', blob)
      emit('update:preview', state.cropperPreview, state.imageType.split('/')[1])
      closeCropper()
    }, state.imageType)
  }
}

function closeCropper(){
  fileupload.value && (fileupload.value.value = '')
  state.openCropper = false
}

function onCropChange(preview: CropperResult) {
  state.cropperPreview = preview
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
  --max-width: 90%;
  --max-height: 80%;
  --height: auto;
}
@media only screen and (min-width: 576px) {
  .crop-modal {
    --max-width: 500px;
  }
}
</style>