<template>
	<ion-modal class="common-modal" :is-open="dialog.open" :show-backdrop="true" @willDismiss="dialog.close">
		<ion-row style="padding: 10px">
			<ion-col size="12">
				<slot>
					<ion-row class="ion-align-items-center">
						<ion-col style="display: flex;" size="auto" v-if="dialog.icon">
							<ion-icon class="icon" :icon="dialog.icon" :color="dialog.iconColor"></ion-icon>
						</ion-col>
						<ion-col style="padding-left: 10px;">
							<div class="title" v-if="dialog.title">{{dialog.title}}</div>
							<div class="description"  v-if="dialog.description">{{dialog.description}}</div>
						</ion-col>
					</ion-row>
				</slot>
			</ion-col>
			<ion-col size="12">
				<ion-button
					v-for="(button, index) in dialog.buttons"
					:key="index"
					size="small"
					:color="button.color"
					@click="onClickButton(button)"
					class="float-right"
					style="margin-right: 15px;"
				>
					{{button.title}}
				</ion-button>
			</ion-col>
		</ion-row>
	</ion-modal>
</template>

<script lang="ts" setup>
import { useDialogStore, Button } from '@/stores/dialog';
import { IonIcon, IonButton, IonCol,  IonRow, IonModal } from '@ionic/vue';

const dialog = useDialogStore()

const emit = defineEmits(['action'])

function onClickButton (button: Button) {
	if (button.action) {
		emit('action', button)
	} else {
		dialog.close()
	}
}

</script>

<style lang="scss" scoped>
  .common-modal {
    --max-width: 90%;
    --height: auto;
  }
  @media only screen and (min-width: 576px) {
    .common-modal {
      --max-width: 400px;
    }
  }
	.icon {
		font-size: 40px;
	}
  .title {
    font-size: 18px;
		font-weight: 500;
		padding-bottom: 5px;
    color: var(--ion-color-dark);
  }
	.description {
		font-size: 15px;
		font-weight: 400;
	}
</style>