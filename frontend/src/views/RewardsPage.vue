<template>
	<ion-page>
		<ion-content class="ion-padding" color="light">
			

			<ion-row class="ion-justify-content-center">

				<ion-col size="8" size-md="8" size-sm="10" size-xs="12">

					<ion-grid>

						<ion-row class="ion-padding ion-justify-content-center row-main">

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
								Hello, {{ user.username }}! Your coins are your shining stars. Keep adding more to light up your path! 
							</ion-col>

							<ion-col size="6">
								<ion-input
									class="custom-input"
									fill="outline"
									v-model="state.points"
									type="number"
									placeholder="Enter Coins"
								>
								</ion-input>
							</ion-col>
						
							<ion-col size="9" class="ion-text-center">
								<ion-button @click="createReedem" size="small">Redeem</ion-button>
							</ion-col>

							<ion-col size="12">
								<ion-accordion-group>
									<ion-accordion value="first">
										<ion-item slot="header" color="light">
											<ion-label>View Coin Activity</ion-label>
										</ion-item>
										<div style="padding: 5px;" slot="content">
											<table style="width:100%">
												<tr>
													<th>Activity</th>
													<th>Status</th>
													<th>Points</th>
													<th></th>
												</tr>
												<tr v-for="(transaction, index) in transactions?.transactions" :key="transaction.id">
													<td>
														<div>
															<span v-if="transaction.type == 'COMPWINNER'">Won Contest</span>
															<span v-if="transaction.type == 'REDEEM'">Redeem</span>
														</div>
														<div style="color: var(--ion-color-medium);font-size: 13px;">{{ formatDateToCustomFormat(transaction.createdAt) }}</div>
													</td>
													<td>
														<span v-if="transaction.status == 'Q'">Pending</span>
														<span v-else-if="transaction.status == 'P'">Processing</span>
														<span v-else-if="transaction.status == 'S'">Success</span>
														<span v-else-if="transaction.status == 'F'">Failed</span>
													</td>
													<td>
														{{ transaction.points }}
													</td>
													<td class="ion-text-center">
														<ion-icon 
															v-if="transaction.status == 'Q'"
															style="font-size: 20px;"
															@click="DeleteReedem(transaction.id)"
															class="cpointer"
															:icon="closeCircleOutline"
														/>
													</td>
												</tr>
												<tr v-if="!loading && !transactions?.transactions.length" >
													<td class="ion-text-center" colspan="4">No Activites</td>
												</tr>
											</table>
										</div>
									</ion-accordion>
								</ion-accordion-group>
							</ion-col>

						</ion-row>

					</ion-grid>

				</ion-col>

				

			</ion-row>

		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonGrid, IonCard, IonPage, IonContent, IonRow, IonCol, IonInput, IonButton, IonIcon, IonImg, IonAccordion, IonAccordionGroup, IonItem } from '@ionic/vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import gql from 'graphql-tag'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { reactive } from 'vue';
import { closeCircleOutline } from 'ionicons/icons'

const user = useUserStore()
const toast = useToastStore()

const state = reactive({
	points: ''
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
									query {
										transactions {
											id,
											points,
											type,
											status,
											createdAt
										}
									}
								`

const { result: transactions, onResult, loading } = useQuery(QUERY)

onResult(({data, loading}) => {

})

function createReedem () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($points: Int!) { 
      createTransaction (
        points: $points,
      ) {
        	ctransaction {
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
				points: parseInt(state.points)
			},
			update: (cache, { data: { createTransaction } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					transactions: [
						createTransaction.ctransaction,
						...data.transactions,
					],
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		toast.$patch({message: 'Request successfully created! Please allow up to two days for processing. Thank you for your patience.', color: 'success', open: true})
		user.$patch({points: data.createTransaction.userpoints})
		state.points = ''
  })

  onError((error: any) => {
		toast.$patch({message: error.message, color: 'danger', open: true})
  })
}

function UpdateReedem () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($points: Int!, $id: ID!) { 
      updateRedeem (
        points: $points,
				id: $id
      ) {
					ctransaction {
						points,
						status
					} 
        }
    }

  `, {
		variables: {points: parseInt(state.points), id: 5}	
	})

  mutate()

  onDone(() => {
  })

  onError((error: any) => {
  })
}

function DeleteReedem (id: string) {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($id: ID!) { 
      deleteTransaction (
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
			update: (cache, { data: { deleteTransaction } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					transactions: data.transactions.filter((reedem: any) => reedem.id != id)
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		user.$patch({points: data.deleteTransaction.userpoints})
		toast.$patch({message: 'Coins were added back', color: 'success', open: true})
  })

  onError((error: any) => {
		toast.$patch({message: error.message, color: 'danger', open: true})
  })
}


</script>

<style scoped>
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
.row-main {
	/* border: 1px solid #dddddd; */
	background-color: var(--ion-color-primary-contrast);
}
</style>