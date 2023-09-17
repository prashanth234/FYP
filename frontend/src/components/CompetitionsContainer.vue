<template>

	<div class="header">
		Contests
	</div>

	<ion-modal class="comp-details-modal" :show-backdrop="true" :is-open="state.showCompDetails" @didDismiss="closeCompDetails">
		<ion-row v-if="state.selectedComp" class="ion-padding">
			<ion-col size="12" class="title ion-text-center">
				{{ state.selectedComp.name }}
			</ion-col>
			<ion-col size="12" style="line-height: 2;">
				🌟 The Quest: {{ state.selectedComp.description }} 🌿 <br>
				🎉 Discover Your Calling: Share Your Passion in Our Rewarding Contest! 🎉 <br>
				🥇 1st Place: <strong>{{ state.selectedComp.points }}</strong> Points <br>
				🥈 2nd Place: <strong>500</strong> Points <br>
				🥉 3rd Place: <strong>200</strong> Points <br>
				🌟 Unveil what drives you! Contest ends on <strong>{{ state.selectedComp.lastDate }}</strong> so showcase your interest. Connect with fellow enthusiasts, accumulate points, and enjoy the journey of this fulfilling contest. Your passion could propel you to the top spot! 🚀
			</ion-col>
			<ion-col class="ion-text-center" size="12">
				<ion-button @click="closeCompDetails" color="light">
					close
				</ion-button>
			</ion-col>
		</ion-row>
	</ion-modal>

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
				:class="{'competition-selected': categoryInfo.selectedComptn?.id == competition.id, 'expired': competition.expired}"
			>	
				<ion-row class="details">
					<ion-col size="auto" class="ion-padding-end">
						<ion-img :src="`media/${competition.image}`"></ion-img>
					</ion-col>
					<ion-col>
						<div class="title">
							{{ competition.name }}
						</div>
						<div class="two-line-ellipsis" :title="competition.description">
							{{ competition.description }}
						</div>
					</ion-col>
				</ion-row>
				<transition name="slide-fade">
					<div v-if="categoryInfo.selectedComptn?.id == competition.id">
						<ion-button
							class="ion-no-margin"
							size="small"
							style="float: right;"
							@click.stop="moreCompDetails(competition)"
							v-if="!competition.expired"
						>
							More
						</ion-button>
						<ion-button
							@click.stop="closeCompetition(competition)"
							class="ion-no-margin cancel-button"
							size="small"
							style="float: right;"
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

import { IonRow, IonCol, IonCard, IonButton, IonImg, IonModal } from '@ionic/vue';
import { useCategoryInfoStore } from '@/stores/categoryInfo';
import { CompetitionInfo } from '@/mixims/interfaces';
import { reactive } from 'vue';

const props = defineProps<{
	vertical: Boolean
}>()

const emit = defineEmits<{
  (e: 'selectCompetition', competition: CompetitionInfo): void;
	(e: 'closeCompetition', competition: CompetitionInfo): void;
}>()

interface State {
	showCompDetails: boolean,
	selectedComp: CompetitionInfo | null
}

const state: State = reactive({
	showCompDetails: false,
	selectedComp: null
})

const categoryInfo = useCategoryInfoStore()

function selectCompetition(competition: CompetitionInfo) {
	emit('selectCompetition', competition)
}

function closeCompetition(competition: CompetitionInfo) {
	emit('closeCompetition', competition)
}

function moreCompDetails(competition: CompetitionInfo) {
	state.showCompDetails = true
	state.selectedComp = competition
}

function closeCompDetails() {
	state.showCompDetails = false
	state.selectedComp = null
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
	.title {
		font-size: 16px;
		font-weight: 600;
		color: var(--ion-color-dark);
		line-height: 1.6;
	}
	.details {
		--ion-grid-column-padding: 0px;
		padding: 13px;	
	}
	&:hover {
  	box-shadow: 0 6px 6px -3px rgba(0,0,0,.2),0 10px 14px 1px rgba(0,0,0,.14),0 4px 18px 3px rgba(0,0,0,.12)!important;
	}
	ion-button {
		--border-radius: 0px;
		&::part(native) {
			border-top-left-radius: 12px;
		}
	}
	ion-img::part(image) {
		width: 50px;
		height: 50px;
		object-fit: cover;
	}
}
.horizantal-row {
	overflow-y: auto;
	.competition {
		min-width: 250px;
	}
}
.header {
	font-size: 18px;
	font-weight: 600;
	padding: 0px 5px 5px 5px;
}
.comp-details-modal {
	--max-width: 100%;
	.title {
		font-size: 20px;
		font-weight: 600;
		color: var(--ion-color-dark);
		line-height: 1.6;
	}
}
@media only screen and (min-width: 576px) {
	// For sm and above screens
	.comp-details-modal {
		--height: auto;
		--max-width: 600px;
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
/* Exit animation class */
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
</style>