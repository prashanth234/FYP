<template>

	<div class="header">
		Contests
	</div>

	<ion-modal
		class="comp-details-modal"
		:show-backdrop="true"
		:is-open="state.showCompDetails"
		@didDismiss="closeCompDetails"
	>
		<ion-row v-if="categoryInfo.selectedComptn" style="overflow: auto; padding: 10px">

			<ion-col size="12" v-if="categoryInfo.selectedComptn.message">
				<alert :message="categoryInfo.selectedComptn.message" type="info"/>
			</ion-col>

			<ion-col size="12" class="title ion-text-center" >
				{{ categoryInfo.selectedComptn.name }}
			</ion-col>

			<ion-col size="12" style="line-height: 1.7;">
				
				<div class="ion-text-start">
					<span class="comp-header">The Quest:</span>
					{{ categoryInfo.selectedComptn.description }}
				</div>

				<div class="ion-text-center points-table">

					<h5>SparkPoints</h5>
					<table class="mlr-auto">
						<tr>
							<th>1st Place</th>
							<th>2nd Place</th>
							<th>3rd Place</th>
						</tr>
						<tr>
							<td>3000</td>
							<td>2000</td>
							<td>1500</td>
						</tr>
					</table>

					<div class="ion-text-start" style="display: flex;">
						<div class="mlr-auto">
							<span class="comp-header">Participation</span>: 250<br>
							<span class="comp-header">Last Date</span>: {{ lastDate }}
						</div>
					</div>
					
				</div>

				<div>
					<span class="comp-header">Key Terms:</span>
					<ol class="ion-no-margin" style="color: grey; line-height: 1.5;">
						<li>To maintain fairness, it is essential that participants create their own content. Entries obtained from the internet will not be taken into consideration.</li>
						<li>Winners will be chosen based on our team’s assessment and the likes received for each post.</li>
						<li>The winner's participation points will be included in the total winning points.</li>
						<li>Participation and Winner points will be credited once the contest ends within 2 business days.</li>
					</ol>
				</div>
			</ion-col>

			<ion-col class="ion-text-center" size="12">
				<ion-button @click="closeCompDetails" color="light">
					close
				</ion-button>
			</ion-col>
		</ion-row>
	</ion-modal>

	<ion-card
		class="note-card"
		color="light"
		v-if="!categoryInfo.competitionSet.length"
	>
		<ion-card-content class="ion-text-center" style="font-weight: 500;">
			Comming Soon!
		</ion-card-content>
	</ion-card>

	<ion-row :class="{'ion-nowrap horizantal-row': !props.vertical}" class="ion-justify-content-start">
		<ion-col
			:size-md="props.vertical ? '12' : 'auto'"
			:size-lg="props.vertical ? '11' : 'auto'"
			:size-xl="props.vertical ? '10' : 'auto'"
			v-for="(competition, index) in categoryInfo.competitionSet"
			:key="index"
		>
			<ion-card
				@click="selectCompetition(competition)"
				class="competition cpointer ion-no-margin"
				:class="{
					'competition-selected': categoryInfo.selectedComptn?.id == competition.id,
					'expired': competition.expired,
					'hovered': state.ihovered == index
				}"
				@mouseover="state.ihovered = index"
      	@mouseout="state.ihovered = null"
			>
				<ion-row class="details ion-nowrap">
					<ion-col size="auto" class="ion-padding-end">
						<ion-img :src="competition.image" :alt="competition.description"></ion-img>
					</ion-col>
					<ion-col style="overflow: hidden;">
						<div class="title overflow-ellipsis">
							{{ competition.name }}
						</div>
						<div class="cat-description" :title="competition.description">
							{{ competition.description }}
						</div>
					</ion-col>
				</ion-row>
				<transition name="slide-fade">
					<div v-if="categoryInfo.selectedComptn?.id == competition.id">
						<ion-button
							class="ion-no-margin float-right"
							size="small"
							@click.stop="moreCompDetails(competition)"
							v-if="!competition.expired"
						>
							More
						</ion-button>
						<ion-button
							@click.stop="closeCompetition(competition)"
							class="ion-no-margin cancel-button float-right"
							size="small"
							color="light"
						>
							Cancel
						</ion-button>
					</div>
				</transition>
			</ion-card>
		</ion-col>
	</ion-row>

</template>

<script lang="ts" setup>

import { IonRow, IonCol, IonCard, IonButton, IonImg, IonModal, IonCardContent } from '@ionic/vue';
import { useCategoryInfoStore } from '@/stores/categoryInfo';
import { CompetitionInfo } from '@/utils/interfaces';
import { reactive, computed } from 'vue';
import { formatDateToCustomFormat  } from '@/utils/common';
import alert from './AlertContainer.vue'

const props = defineProps<{
	vertical: Boolean
}>()

const emit = defineEmits<{
  (e: 'selectCompetition', competition: CompetitionInfo): void;
	(e: 'closeCompetition', competition: CompetitionInfo): void;
}>()

interface State {
	showCompDetails: boolean,
	ihovered: number | null
}

const state: State = reactive({
	showCompDetails: false,
	ihovered: null
})

const points = computed(() => {
	if (categoryInfo.selectedComptn) {
		// return categoryInfo.selectedComptn.points.split(',').sort((a, b) => {
		// 	return parseInt(b) - parseInt('a')
		// })
		const [firstplace, secondplace, thridplace, pariticipation] = categoryInfo.selectedComptn.points.split(',')
		return {
			'1st Place': firstplace,
			'2nd Place': secondplace,
			'3rd Place': thridplace,
			'Participation': pariticipation
		}
	}
	return []
})

const lastDate = computed(() => {
	return categoryInfo.selectedComptn ? formatDateToCustomFormat(categoryInfo.selectedComptn.lastDate) : ''
})

const categoryInfo = useCategoryInfoStore()

function selectCompetition(competition: CompetitionInfo) {
	emit('selectCompetition', competition)
}

function closeCompetition(competition: CompetitionInfo) {
	emit('closeCompetition', competition)
	state.ihovered = null
}

function moreCompDetails(competition: CompetitionInfo) {
	state.showCompDetails = true
}

function closeCompDetails() {
	state.showCompDetails = false
}

</script>

<style scoped lang="scss">
.competition-selected {
  border-left: 3px solid var(--ion-color-primary-tint);
	.details {
		padding-bottom: 10px;
	}
	&.expired {
		border-left: 3px solid var(--ion-color-medium-tint);
	}
}
.competition {
	min-height: 78px;
	max-width: 300px;
	overflow: hidden;

	.title {
		font-size: 16px;
		font-weight: 580;
		color: var(--ion-color-dark);
		padding-bottom: 2px;
	}
	.details {
		--ion-grid-column-padding: 0px;
		padding: 10px;	
	}
	ion-button {
		--border-radius: 0px;
		&::part(native) {
			border-top-left-radius: 12px;
		}
	}
	ion-img::part(image) {
		width: 55px;
		height: 55px;
		object-fit: cover;
		border-radius: 4px;
	}
}
.hovered {
	// box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
	box-shadow: rgba(0, 0, 0, 0.15) 0px 2px 8px;
}
.horizantal-row {
	overflow-y: auto;
	.competition {
		min-width: 250px;
	}
}
.header {
	font-size: 18px;
	font-weight: 580;
	padding: 0px 5px 5px 5px;
}
.comp-details-modal {
	--max-width: 90%;
	--height: 80vh;

	.title {
		font-size: 19px;
		font-weight: 550;
		color: var(--ion-color-dark);
		line-height: 1.6;
	}
	.comp-header {
		font-size: 16px;
		font-weight: 550;
	}
}
@media only screen and (min-width: 576px) {
	// For sm and above screens
	.comp-details-modal {
		--height: min(580px, 95vh);
		--min-width: 800px !important;
		--max-width: 800px !important;
	}
}
@media only screen and (max-width: 576px) {
	// For small screens
	.competition {
		.title {
			font-size: 15px;
		}
	}	
	.header {
		font-size: 17px;
	}
}

.slide-fade-enter-active {
  animation: slide-fade-in 0.5s ease forwards;
}
@keyframes slide-fade-in {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// /* Exit animation class */
// .slide-fade-leave-active {
//   animation: slide-fade-out 0.3s ease forwards;
// }

// /* Keyframes for the exit animation */
// @keyframes slide-fade-out {
//   from {
//     opacity: 1;
//     transform: translateY(0);
//   }
//   to {
//     opacity: 0;
//     transform: translateY(-20px);
//   }
// }

// Hide scorll bar for competitions 
::-webkit-scrollbar {
  width: 0.1rem;
  height: 0.1rem;
}
::-webkit-scrollbar-thumb {
  background-color: transparent;
}
::-webkit-scrollbar-track {
  background-color: transparent;
}

.points-table {
	width: 100%;
	border-collapse: collapse;
	margin-top: 10px;
	margin-bottom: 10px;
	table {
		margin-bottom: 10px;
	}
	th, td {
		border: 1px solid #ddd;
		padding: 5px;
		text-align: center;
	}
	th {
		background-color: var(--ion-color-primary-tint);
		color: white;
		font-weight: 550;
	}
}

</style>