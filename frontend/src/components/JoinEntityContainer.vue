<template>
  <!-- Join Entity Model -->
  <ion-modal
    class="join-entity-modal"
    :show-backdrop="true"
    :backdropDismiss="false"
    :is-open="props.show"
    @didDismiss="close"
  >

    <ion-toolbar color="light">
      <ion-title>Join Entity</ion-title>
      <ion-buttons slot="end">
        <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="close"></ion-icon>
      </ion-buttons>
    </ion-toolbar>

    <ion-grid class="entity-grid">

      <ion-row class="ion-text-center">

        <ion-col size="12" v-if="state.message">
          <alert :message="state.message" :type="state.msgType"/>
        </ion-col>

        <ion-col size="12">

          <div class="label">
            Enter the code shared with your entity
          </div>

          <ion-input
            class="custom-input"
            v-model="state.code"
            type="text"
            placeholder="Code"
          >
          </ion-input>

        </ion-col>

        <ion-col size="12" class="text-bold">

          (OR)

        </ion-col>

        <ion-col size="12" class="ion-text-center">

          <div class="label">
            Upload any ID that shows you belong to the entity
          </div>

          <FileUpload
            v-model="state.file"
            :simple="true"
            :cropable="false"
            file-type="image/*,.pdf"
          >
            <template #handler="{selectImage, loading}">
              <ion-button
                @click="selectImage()"
                for="file-upload"
                size="small"
                fill="outline"
                color="primary"
                :disabled="loading || state.loading"
              >
                <ion-spinner 
                  class="button-loading-small"
                  v-if="loading"
                  name="crescent"
                />
                <span v-else>
                  Upload File
                </span>
              </ion-button>
            </template>
          </FileUpload>

          <div class="uploaded-filename">
            {{ state.file ? state.file.name : '' }}
          </div>

        </ion-col>

        <div style="padding: 0px 15px;">
          <errors :errors="state.errors"/>
        </div>

        <ion-col size="12" style="padding-top: 10px">

          <ion-button
            color="success"
            size="small"
            style="width: 120px;"
            :disabled="state.loading"
            @click="submit"
          >
            <ion-spinner 
              class="button-loading-small"
              v-if="state.loading"
              name="crescent"
            />
            <span v-else>
              Submit
            </span>
          </ion-button>

        </ion-col>

      </ion-row>

    </ion-grid>
  </ion-modal>
</template>

<script lang="ts" setup>
import { IonButton, IonModal, IonSpinner, IonGrid, IonRow, IonCol, IonInput, IonToolbar, IonTitle, IonButtons, IonIcon } from '@ionic/vue';
import FileUpload from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue';
import { closeOutline } from 'ionicons/icons'
import alert from './AlertContainer.vue'
import { useToastStore } from '@/stores/toast'
import errors from '@/components/ErrorContainer.vue'
import { useJoinEntityAPI } from '@/composables/entity'

const props = defineProps({
  show: Boolean,
  entity: String
})

const emit = defineEmits(['update:show'])

const toast = useToastStore()

interface State {
  code: string,
  file: any,
  loading: boolean,
  message: string
  msgType: string,
  errors: string[]
}

const state: State = reactive({
  code: '',
  file: null,
  loading: false,
  message: '',
  msgType: '',
  errors: []
})

const ENTIY_ERROR = 'Enter code or upload ID to continue!'

function close() {
  emit('update:show', false)
}

function submit() {
  state.errors = []

  if (!state.code && !state.file) {
    state.errors.push(ENTIY_ERROR)
    return
  }

  state.loading = true

  let variables = {
    file: state.file || undefined,
    code: state.code,
    entityId: props.entity
  }

  const { mutate, onDone, onError } = useJoinEntityAPI()
  mutate(variables)

  onDone(({data}) => {
    if (data.joinEntity.success) {
      toast.$patch({message: data.joinEntity.message, color: 'success', open: true})
      close()
    } else {
      state.errors.push(data.joinEntity.message)
    }
    state.code = ''
    state.loading = false
  })

  onError(() => {
    toast.$patch({message: 'Failed to process request, please try again.', color: 'danger', open: true})
    state.loading = false
  })
}

</script>

<style lang="scss" scoped>
  .join-entity-modal {
    // For xs screens
    --max-width: 100%;
  }
  @media only screen and (min-width: 576px) {
    // For sm and above screens
    .join-entity-modal {
      --height: auto;
      --max-width: 350px;
    }
  }
  .entity-grid {
    --ion-grid-padding: 15px;
    --ion-grid-column-padding: 20px;

    .label {
      padding-bottom: 15px;
    }
  }
</style>