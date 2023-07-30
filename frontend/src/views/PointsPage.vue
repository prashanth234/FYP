<template>
	<ion-page>
		<ion-content class="ion-padding">
			<h1>hello</h1>
		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent } from '@ionic/vue';
</script>

<style lang="scss" scoped>
ion-content::part(scroll) {
  padding-top: 0px;
}
</style>