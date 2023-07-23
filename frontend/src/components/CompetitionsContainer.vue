<template>
	<ion-card class="border-radius-std">

		<ion-card-header style="padding-bottom: 5px">
				<ion-card-title>Competitions</ion-card-title>
		</ion-card-header>

		<ion-row :class="{'ion-nowrap horizantal-row': !props.vertical}">
			<ion-col
				:size="props.vertical ? '12' : 'auto'"
				v-for="(competition, index) in categoryInfo.competitionSet"
				:key="index"
			>
				<ion-card
					@click="selectCompetition(competition)"
					class="competition cpointer"
					:class="{'competition-selected': categoryInfo.selectedComptn?.id == competition.id, 'horizantal-card' : !props.vertical}"
				>
					<ion-card-header>
						<ion-card-title>{{ competition.name }}</ion-card-title>
					</ion-card-header>

					<ion-card-content>
						<p class="two-line-ellipsis" :title="competition.description">
								{{ competition.description }}
						</p>
					</ion-card-content>
				</ion-card>
			</ion-col>
		</ion-row>

	</ion-card>
</template>

<script lang="ts" setup>

import { IonRow, IonCol, IonCard, IonCardHeader, IonCardTitle, IonCardContent } from '@ionic/vue';
import { useCategoryInfoStore } from '@/stores/categoryInfo';
import { CompetitionInfo } from '@/mixims/interfaces';

const props = defineProps<{
	vertical: Boolean
}>()

const emit = defineEmits<{
  (e: 'selectCompetition', competition: CompetitionInfo): void;
}>()

const categoryInfo = useCategoryInfoStore()

function selectCompetition(competition: CompetitionInfo) {
	emit('selectCompetition', competition)
}

</script>

<style scoped>
.competition-selected {
  border: 1px solid var(--ion-color-primary)
}
.competition:hover {
  box-shadow: 0 6px 6px -3px rgba(0,0,0,.2),0 10px 14px 1px rgba(0,0,0,.14),0 4px 18px 3px rgba(0,0,0,.12)!important;
  /* border: 1px solid var(--ion-color-primary); */
  /* box-shadow: inset 0 0 0 3px #eee; */
}
.horizantal-card {
  width: 150px;
  height: 120px;
}
.horizantal-row {
	overflow-y: auto;
	padding: 5px
}
</style>