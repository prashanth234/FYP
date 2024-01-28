<template>
	<ion-page>
		<ion-content>

			<ion-grid style="max-width: 700px; margin-top:20px">

				<ion-row class="ion-padding ion-justify-content-center background-contrast">

					<ion-col size="auto" class="ion-align-self-center" style="font-size: 20px; font-weight: 580;">
						We're here to support you!
					</ion-col>

					<ion-col size="12" class="ion-text-center" style="font-weight: 500;">
						Need assistance or have feedback? Share your thoughts with us in the text box below and submit.
					</ion-col>

					<!-- <ion-col size="10" size-md="10" size-sm="10" size-xs="12">
						<ion-input
							class="custom-input"
							v-model="state.contact"
							v-if="!user.success"
							label="Email/Phone"
						>
						</ion-input>
					</ion-col> -->

					<ion-col size="10" size-md="10" size-sm="10" size-xs="12">
						<ion-textarea
							class="custom-textarea support-textarea"
							style="--padding-top: 10px;"
							auto-grow
							v-model="state.description"
							type="number"
							placeholder="Enter Here"
						>
						</ion-textarea>
					</ion-col>
				
					<ion-col size="9" class="ion-text-center">
						<ion-button
							@click="createSupport"
							class="submit-button"
							:disabled="disable"
						>
							Submit
						</ion-button>
					</ion-col>

				</ion-row>

			</ion-grid>

		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonGrid, IonPage, IonContent, IonRow, IonCol, IonTextarea, IonButton, IonInput } from '@ionic/vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import gql from 'graphql-tag'
import { useMutation } from '@vue/apollo-composable'
import { reactive, computed } from 'vue';
import { scrollTop } from '@/composables/scroll'

scrollTop()

const user = useUserStore()
const toast = useToastStore()

const state = reactive({
	description: '',
	contact: ''
})

const disable = computed(() => {
	if(user.success) {
		return !state.description
	} else {
		return !state.description || !state.contact
	}
})

function createSupport () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($description: String!, $contact: String) { 
      createSupport (
        description: $description,
				contact: $contact
      ) {
        	success
        }
    }

  `, () => ({
			variables: {
				description: state.description,
				contact: state.contact || undefined
			}
		})
	)

  mutate()

  onDone(({data}) => {
		toast.$patch({message: "Thank you for reaching out! We'll get back to you shortly.", color: 'success', open: true})
		state.description = ''
		state.contact = ''
  })

  onError((error: any) => {
		toast.$patch({message: error.message, color: 'danger', open: true})
  })
}

</script>

<style scoped lang="scss">
ion-grid {
	--ion-grid-column-padding: 10px;
}
.submit-button {
  height: 32px;
	width: 150px;
}
@media only screen and (min-width: 576px) {
	
}
</style>
<style lang="scss">
@media only screen and (max-width: 992px) {
	// For xs, sm, md  screens
	.support-textarea {
		label {
			max-height: calc(100vh - 500px) !important;
		}
	}
}
.support-textarea {
  label {
    max-height: calc(100vh - 350px);
		overflow-y: auto;
  }
}
</style>