<template>
	<ion-card class="border-radius-std" v-if="categoryInfo.selectedComptn">
		<ion-accordion-group>
			<ion-accordion value="first">
				<ion-item slot="header" color="light">
					<ion-label>Competition Details</ion-label>
				</ion-item>
				<div class="ion-padding" slot="content">
					<table style="width:100%">
						<tr>
							<td class="header">Description</td>
							<td>{{ categoryInfo.selectedComptn.description }}</td>
						</tr>
						<tr>
							<td class="header">Last Date</td>
							<td>{{ categoryInfo.selectedComptn.lastDate }}</td>
						</tr>
						<tr>
							<td class="header">Points</td>
							<td>{{ categoryInfo.selectedComptn.points }}</td>
						</tr>
					</table>
				</div>
			</ion-accordion>
		</ion-accordion-group>
  </ion-card>
</template>

<script lang="ts" setup>

import { IonCard, IonAccordion, IonAccordionGroup, IonItem, IonLabel } from '@ionic/vue';
import { useCategoryInfoStore } from '@/stores/categoryInfo';

const categoryInfo = useCategoryInfoStore()

</script>

<style scoped>
table, th, td {
  border-collapse: collapse;
  padding-bottom: 13px;
  padding-top: 13px;
  color: var(--ion-color-dark);
}
tr {
  border-bottom: 0.5px solid var(--ion-color-medium);
}
tr:last-child {
  border-bottom: 0px;
}
table .header {
  width: 150px;
}
</style>