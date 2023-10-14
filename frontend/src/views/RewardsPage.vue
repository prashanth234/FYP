<template>
	<ion-page>
		<ion-content color="light">

			<ion-grid style="max-width: 700px;">

				<ion-row class="ion-padding ion-justify-content-center primary-contrast">

					<ion-col size="12">
						<ion-row class="ion-no-padding ion-justify-content-center">
							<ion-col size="auto">
								<ion-img
									style="width: 30px; height: 30px;"
									src="/static/core/coins.png"
								></ion-img>
							</ion-col>
							<ion-col size="auto" class="ion-align-self-center" style="font-size: 20px; font-weight: 600;">
								{{ user.points}} Coins
							</ion-col>
						</ion-row>
					</ion-col>

					<ion-col size="12" class="ion-text-center" style="font-weight: 500;">
						<!-- Hello, {{ user.username }}! Your coins are your shining stars. Keep adding more to light up your path!  -->
						Your coins, your rewards! Select a gift card to treat yourself.
					</ion-col>

					<ion-col size="12">

						<Transition name="slide-fade" mode="out-in">

							<div v-if="state.selReward > -1">
								<ion-row>
									<ion-col size-sm="auto" size-xs="12" style="margin-right: 10px;">
										<ion-img class="reward-image" :src="`/media/${rewards.rewards[state.selReward].image}`">
										</ion-img>
										<div class="reward-title">
											{{rewards.rewards[state.selReward].name}}
										</div>
									</ion-col>
									<ion-col>
										<ion-select
											fill="outline"
											class="custom-input"
											v-model="state.points"
											placeholder="Select"
											label="Amount"
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
										class="grid-item cpointer"
										v-for="(reward, index) in rewards?.rewards"
										@click="selectReward(index)"
										:key="index"
									>

										<ion-img :src="`/media/${reward.image}`">
										</ion-img>

										<div class="reward-title">
											{{reward.name}}
										</div>

									</div>

								</div>

								<!-- Coin activity -->
								<ion-accordion-group>
									<ion-accordion value="first">
										<ion-item slot="header" color="light">
											<ion-label>View Coin Activity</ion-label>
										</ion-item>
										<div style="padding: 5px;overflow: auto;" slot="content">
											<table style="width:100%">
												<tr>
													<th style="min-width: 150px;">Activity</th>
													<th style="min-width: 150px;">Status</th>
													<th style="min-width: 100px;">Points</th>
													<th class="ion-text-center">Action</th>
												</tr>
												<tr v-for="(coinactivity, index) in coinactivities?.coinactivities" :key="coinactivity.id">
													<td>
														<div>
															<span v-if="coinactivity.type == 'COMPWINNER'">Won Contest</span>
															<span v-if="coinactivity.type == 'REDEEM'">Redeem</span>
														</div>
														<div style="color: var(--ion-color-medium);font-size: 13px;">{{ formatDateToCustomFormat(coinactivity.createdAt) }}</div>
													</td>
													<td>
														<span v-if="coinactivity.status == 'Q'">Pending</span>
														<span v-else-if="coinactivity.status == 'P'">Processing</span>
														<span v-else-if="coinactivity.status == 'S'">Success</span>
														<span v-else-if="coinactivity.status == 'F'">Failed</span>
													</td>
													<td>
														{{ coinactivity.points }}
													</td>
													<td class="ion-text-center">
														<ion-icon 
															v-if="coinactivity.status == 'Q'"
															style="font-size: 20px;"
															@click="deleteReedem(coinactivity.id)"
															class="cpointer"
															:icon="closeCircleOutline"
														/>
													</td>
												</tr>
												<tr v-if="!loading && !coinactivities?.coinactivities.length" >
													<td class="ion-text-center" colspan="4">No Activites</td>
												</tr>
											</table>
										</div>
									</ion-accordion>
								</ion-accordion-group>

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
import { closeCircleOutline } from 'ionicons/icons'
import { scrollTop } from '@/composables/scroll'

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

scrollTop()

const user = useUserStore()
const toast = useToastStore()

const state: State = reactive({
	points: 0,
	selReward: -1,
	loading: false,
	denominations: []
})

function formatDateToCustomFormat(isoDate: string): string {
  const date = new Date(isoDate);

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  };

  return date.toLocaleDateString(undefined, options);
}

const QUERY = gql`
									query CoinActivities {
										coinactivities {
											id,
											points,
											type,
											status,
											createdAt
										}
									}
								`

const { result: coinactivities, onResult, loading } = useQuery(QUERY)

onResult(({data, loading}) => {

})

function createReedem (reward: string) {
	state.loading = true
	console.log

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
						type,
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


</script>

<style scoped>
.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
	grid-gap: 20px;
	/* Ensure all rows have the same height */
	grid-auto-rows: auto;
	padding: 5px;
	margin-bottom: 15px;
}
.grid-item {
  border: 1px solid var(--ion-color-light-shade);
	color: var(--ion-text-color);
	border-radius: 10px;
	padding: 10px;
	display: flex;
	flex-direction: column;
	text-align: center;
}
.grid-item:hover {
  box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
}
.reward-title {
	padding-top: 5px;
	text-align: center;
}
.reward-image {
	width: 100px;
	height: 100px;
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
</style>