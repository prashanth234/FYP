<template>
	<ion-page>
		<ion-content>

			<ion-grid style="max-width: 700px;margin-top: 20px">

				<ion-row class="ion-padding ion-justify-content-center background-contrast">

					<ion-col size="12">
						<ion-row class="ion-no-padding ion-justify-content-center">
							<ion-col size="auto" style="padding-right: 0px;">
								<ion-img
									style="width: 30px; height: 30px;"
									src="/static/core/coins.png"
									alt="SparkPoints"
								></ion-img>
							</ion-col>
							<ion-col size="auto" class="ion-align-self-center" style="font-size: 19px; font-weight: 550;">
								{{ user.points}} SparkPoints
							</ion-col>
						</ion-row>
					</ion-col>

					<ion-col size="12" class="ion-text-center" style="font-weight: 500;">
						<!-- Hello, {{ user.username }}! Your coins are your shining stars. Keep adding more to light up your path!  -->
						Your points, your rewards! Select a gift card to treat yourself.
					</ion-col>

					<ion-col size="12">

						<Transition name="slide-fade" mode="out-in">

							<div v-if="state.selReward > -1">
								<ion-row class="ion-justify-content-center">
									<ion-col size="auto">
										<div class="logo">
											<ion-img
												class="reward-image"
												:src="rewards.rewards[state.selReward].image"
												:alt="rewards.rewards[state.selReward].name"
											>
											</ion-img>
										</div>
										<!-- <div class="reward-title">
											{{rewards.rewards[state.selReward].name}}
										</div> -->
									</ion-col>
									<ion-col size-xs="12" size-sm="auto">
										<ion-select
											class="custom-select"
											v-model="state.points"
											placeholder="Select Amount"
											label-placement="stacked"
											label=""
											interface="popover"
										>
											<ion-select-option
												v-for="denom in state.denominations"
												:key="denom.points"
												:value="denom.points"
											>
												{{ denom.text }}
											</ion-select-option>
										</ion-select>

										<div class="redeem-note">
											Note: Once SparkPoints are redeemed, they can't be cancelled.
										</div>

										<div style="text-align: end; margin-top: 20px" class="action-buttons">
											<ion-button
											 	class="auth-button ion-margin-end"
												color="light"
												@click="cancelReward"
												:disabled="state.loading"
											>
												Cancel
											</ion-button>
											<ion-button
											 	class="auth-button"
												@click="createReedem(rewards.rewards[state.selReward].id)"
												:disabled="!state.points || state.loading"
											>
												<ion-spinner 
													class="button-loading-small"
													v-if="state.loading"
													name="crescent"
												/>
												<span v-else>
													Redeem
												</span>
											</ion-button>
										</div>
										
									</ion-col>
								</ion-row>
							</div>

							<div v-else>

								<!-- Gift cards grid -->
								<div class="grid-container">

									<div
										class="grid-item cpointer logo"
										v-for="(reward, index) in rewards?.rewards"
										@click="selectReward(index)"
										:key="index"
									>

										<ion-img :src="reward.image" :alt="reward.name">
										</ion-img>

										<!-- <div class="reward-title">
											{{reward.name}}
										</div> -->

									</div>

								</div>

								<!-- Coin activity -->
								<ion-accordion-group>
									<ion-accordion value="first">
										<ion-item slot="header" color="light">
											<ion-label style="font-weight: 550;">View Points Activity</ion-label>
										</ion-item>
										<div style="padding: 5px; overflow: auto; background-color: var(--ion-card-background)" slot="content">
											<table style="width:100%;">
												<tr>
													<th style="min-width: 200px;">Activity</th>
													<th style="min-width: 100px;" class="ion-text-end">Points</th>
												</tr>
												<tr v-for="(coinactivity, index) in coinactivities?.coinactivities" :key="coinactivity.id">
													<td>
														<div style="font-size: 15px;">{{ coinactivity.description }}</div>
														<div
															style="color: var(--ion-color-medium);font-size: 12px;">
															{{ formatDateToCustomFormat(coinactivity.createdAt) }}
														</div>
													</td>
													<td
														class="ion-text-end"
														:class="{
															'points-pending': coinactivity.status == 'Q',
															'points-failure': coinactivity.status == 'F',
															'points-add': coinactivity.points > 0,
															'points-minus': coinactivity.points < 0
														}"
														style="font-weight: 580; font-size: 15px;"
													>
														<ion-row class="points ion-nowrap ion-align-items-center" style="float: right;">
															<ion-col class="ion-align" size="auto">
																<ion-icon 
																	v-if="coinactivity.status == 'Q'"
																	class="icon"
																	style="font-size: 17px;"
																	:icon="hourglassOutline"
																/>
																<ion-icon 
																	v-else-if="coinactivity.status == 'F'"
																	class="icon cpointer"
																	style="font-size: 17px;"
																	:icon="alertCircleOutline"
																	@click="failureMessage(coinactivity.comments)"
																/>
															</ion-col>
															<ion-col size="auto" style="padding-bottom: 5px;">
																{{ `${coinactivity.points > 0 ? '+': ''}${coinactivity.points}` }}
															</ion-col>
														</ion-row>
													</td>
												</tr>
												<tr v-if="!loading && !coinactivities?.coinactivities.length" >
													<td class="ion-text-center" colspan="4">No Activites</td>
												</tr>
											</table>
										</div>
									</ion-accordion>
								</ion-accordion-group>

								<!-- Faqs -->
								
								<ion-row class="ion-padding-top">
									
									<ion-col size="12" style="font-weight: 580;">
										Frequently Asked Questions
									</ion-col>

									<ion-col size="12" v-for="(faq, index) in faqs?.faqs" :key="index" style="font-size: 15px;">

										<div style="font-weight: 580;">
											Q: {{ faq.question }}
										</div>

										<div>
											A: {{ faq.answer }}
										</div>

									</ion-col>
								</ion-row>

							</div>

						</Transition>

					</ion-col>

				</ion-row>

			</ion-grid>

		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonLabel, IonGrid, IonPage, IonContent, IonRow, IonCol, IonSelect, IonButton, IonIcon, IonImg, IonAccordion, IonAccordionGroup, IonItem, IonSelectOption, IonSpinner } from '@ionic/vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import gql from 'graphql-tag'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { reactive } from 'vue';
import { hourglassOutline, alertCircleOutline } from 'ionicons/icons'
import { scrollTop } from '@/composables/scroll'
import { formatDateToCustomFormat  } from '@/utils/common';
import { onBeforeRouteLeave } from 'vue-router'
import { getQuery } from '@/composables/coinActivity'
import { useDialogStore } from '@/stores/dialog'

const dialog = useDialogStore();

interface Denomination {
	points: number,
	rupees: number,
	text: string
}

interface State {
	points: number,
	selReward: number,
	loading: boolean,
	denominations: Denomination[]
}

onBeforeRouteLeave(() => {
  state.points = 0
	state.selReward = -1
})

scrollTop()

const user = useUserStore()
const toast = useToastStore()

const state: State = reactive({
	points: 0,
	selReward: -1,
	loading: false,
	denominations: []
})

// Also update in create post
const QUERY = getQuery()

const { result: coinactivities, onResult, loading } = useQuery(QUERY)

onResult(({data, loading}) => {

})

function failureMessage(msg: string) {
  const buttons = [
    {title: 'Close', color: 'light'}
  ]

  dialog.show(
    "",
    msg || "Apologies, but we couldn't process your request. Please contact our support if you have any concerns or questions.",
    buttons,
    alertCircleOutline,
    'danger'
  )
}

function createReedem (reward: string) {
	state.loading = true

	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation createCoinactivity ($points: Int!, $reward: ID!) { 
      createCoinactivity (
        points: $points,
				reward: $reward
      ) {
					coinactivity {
						points,
						status,
						createdAt,
						description,
						id
					},
					userpoints
        }
    }

  `, () => ({
			variables: {
				points: state.points,
				reward
			},
			update: (cache, { data: { createCoinactivity } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					coinactivities: [
						createCoinactivity.coinactivity,
						...data.coinactivities,
					],
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		toast.$patch({message: 'Request successfully created! Please allow up to two days for processing. Thank you for your patience.', color: 'success', open: true})
		user.$patch({points: data.createCoinactivity.userpoints})
		state.points = 0
		cancelReward()
  })

  onError((error: any) => {
		toast.$patch({message: error.message, color: 'danger', open: true})
		state.loading = false
  })
}

function UpdateReedem () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($points: Int!, $id: ID!) { 
      updateRedeem (
        points: $points,
				id: $id
      ) {
					updateCoinactivity {
						points,
						status
					} 
        }
    }

  `, {
		variables: {points: state.points, id: 5}	
	})

  mutate()

  onDone(() => {
  })

  onError((error: any) => {
  })
}

function deleteReedem (id: string) {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($id: ID!) { 
      deleteCoinactivity (
				id: $id
      ) {
          success,
					userpoints
        }
    }

  `, () => ({
			variables: {
				id
			},
			update: (cache, { data: { deleteCoinactivity } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					coinactivities: data.coinactivities.filter((reedem: any) => reedem.id != id)
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		user.$patch({points: data.deleteCoinactivity.userpoints})
		toast.$patch({message: 'Reedem canceled! Coins were added back', color: 'success', open: true})
  })

  onError((error: any) => {
		toast.$patch({message: error.message, color: 'danger', open: true})
  })
}

function cancelReward() {
	state.points = 0
	state.selReward = -1
	state.loading = false
}

function selectReward(index: number) {
	const {points, pointsvalue} = rewards.value.rewards[index]
	state.denominations = points.split(',').map((point: string) => {
		const points = parseInt(point)
		const rupees = points / (pointsvalue || 10)
		return {text: `₹${rupees} (${points} points)`, points, rupees}
	})
	state.selReward = index
}

const { result: rewards, onResult: rewardsResult, onError } = useQuery(gql`
                              query rewards {
                                rewards {
																	id,
																	name,
																	type,
																	points,
																	image,
																	pointsvalue
																}
                              }
                            `)

onError(() => {
})

const { result: faqs, onResult: faqsResult ,onError: faqsError } = useQuery(gql`
                              query rewards {
																faqs (qtype: "REWARD") {
																	question,
																	answer
																}
                              }
                            `)


</script>

<style scoped lang="scss">
.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
	grid-gap: 20px;
	/* Ensure all rows have the same height */
	grid-auto-rows: auto;
	padding: 5px;
	margin-bottom: 20px;
}
.grid-item {
	color: var(--ion-text-color);
	display: flex;
	flex-direction: column;
	text-align: center;
}
.logo {
	border: 1px solid var(--ion-color-light-shade);
	border-radius: 7px;
	padding: 10px;
	background-color: #ffffff;
}
.grid-item:hover {
  box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
}
.reward-title {
	padding-top: 5px;
	text-align: center;
}
.reward-image {
	width: 80px;
	height: 80px;
}
table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border-bottom: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}
th {
	font-weight: 450;
}
ion-grid {
	--ion-grid-column-padding: 10px;
}
.slide-fade-enter-active {
  transition: all 0.2s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
}
@media only screen and (max-width: 576px) {
	.reward-image {
		margin: auto;
	}
	.action-buttons {
		text-align: center !important;
	}
	.grid-item {
		padding: 15px;
	}
}
.redeem-note {
	padding: 5px;
	padding-top: 8px;
	font-size: 14px;
	color: var(--ion-color-medium-shade);
}
.points-add {
	color: var(--ion-color-success-shade);
}
.points-minus {
	color: var(--ion-color-danger);
}
.points-pending {
	color: var(--ion-color-medium-shade);
}
.points {
	--ion-grid-padding: 0px;
	--ion-grid-column-padding: 0px;
}
.points-failure {
	color: var(--ion-color-medium-shade);
	.icon {
		color: var(--ion-color-danger)
	}
	.icon:hover {
		color: red;
	}
}
</style>