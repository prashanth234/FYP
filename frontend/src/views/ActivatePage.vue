<template>

    <ion-page>
      <ion-content>

        <ion-loading :isOpen="state.loading" message="Verifying"></ion-loading>

        <ion-grid v-if="!state.loading">
          <ion-row class="ion-text-center ion-padding" style="padding-top: 100px;">

              <ion-col v-if="state.success" size="12">
                <h3>{{state.message}}</h3>
              </ion-col>

              <ion-col v-else size="12">
                <h3>{{state.message}}</h3> 
              </ion-col>

          </ion-row>
        </ion-grid>
      </ion-content>
    </ion-page>

</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { reactive } from 'vue'
import { IonPage, IonContent, IonGrid, IonRow, IonCol, IonLoading, IonButton, useIonRouter } from '@ionic/vue'
import store from '@/vuex';
import { useToastStore } from '@/stores/toast'


const router = useRoute();
const ionRouter = useIonRouter();
const toast = useToastStore();

const token = router.params.token

const state = reactive({
  success: false,
  message: '',
  loading: true
})

try {
  const { mutate, onDone } = useMutation(gql`    
    
    mutation ($token: String!) {
        verifyAccount (
            token: $token,
        ) {
            success, errors
        }
    }

  `)

  mutate({token})

  onDone(({data: {verifyAccount}}) => {
    const {success, errors} = verifyAccount
    state.success = success
    if (success) {
      state.message = 'Account verified successfully.'
      // goHome()
    } else {
      state.message = errors.nonFieldErrors[0].message
    }
    state.loading = false
  })

} catch (error) {
  console.error(error)
}

function goHome () {
  toast.$patch({message: "Account verified successfully.", color: 'success', open: true})
  ionRouter.push('/')
}

</script>