<template>
	<ion-page>
		<ion-content class="ion-padding">
			<h1>{{`Hello ${user.username}, you have ${user.points} points`}}</h1>

			<ion-row>

				<ion-col size="6">
					<ion-input v-model="state.points" label="Points" type="number" placeholder="0"></ion-input>
				</ion-col>
				
				<ion-col size="6">
					<ion-button @click="createReedem">Submit</ion-button>
				</ion-col>

				<ion-col size="6">
					<table style="width:100%">
						<tr>
							<th>Requested At</th>
							<th>Points</th>
							<th>Status</th>
							<th>Cancel</th>
						</tr>
						<tr v-for="(redemption, index) in redemptions?.redemptions" :key="redemption.id">
							<td>
								{{ redemption.createdAt.slice(0, 19) }}
							</td>
							<td>
								{{ redemption.points }}
							</td>
							<td>
								<span v-if="redemption.status == 'Q'">Pending</span>
								<span v-else-if="redemption.status == 'P'">Processing</span>
								<span v-else-if="redemption.status == 'R'">Redeemed</span>
								<span v-else-if="redemption.status == 'F'">Failed</span>
							</td>
							<td class="ion-text-center">
								<ion-icon 
									v-if="redemption.status == 'Q'"
									style="font-size: 20px;"
									@click="DeleteReedem(redemption.id)"
									class="cpointer"
									:icon="closeCircleOutline"
								/>
							</td>
						</tr>
						<tr v-if="!loading && !redemptions?.redemptions.length" >
							<td class="ion-text-center" colspan="4">No Redeemptions</td>
						</tr>
					</table>
				</ion-col>

			</ion-row>

		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonRow, IonCol, IonInput, IonButton, IonIcon } from '@ionic/vue';
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

const QUERY = gql`
									query {
										redemptions {
											id,
											status,
											points,
											createdAt
										}
									}
								`

const { result: redemptions, onResult, loading } = useQuery(QUERY)

onResult(({data, loading}) => {

})

function createReedem () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($points: Int!) { 
      createRedeem (
        points: $points,
      ) {
        	redeem {
						points,
						status,
						createdAt,
						id
					},
					userpoints
        }
    }

  `, () => ({
			variables: {
				points: parseInt(state.points)
			},
			update: (cache, { data: { createRedeem } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					redemptions: [
						...data.redemptions,
						createRedeem.redeem,
					],
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		user.$patch({points: data.createRedeem.userpoints})
		state.points = '0'
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
          redeem {
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
      deleteRedeem (
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
			update: (cache, { data: { deleteRedeem } }) => {
				let data:any = cache.readQuery({ query: QUERY })
				data = {
					...data,
					redemptions: data.redemptions.filter((reedem: any) => reedem.id != id)
				}
				cache.writeQuery({ query: QUERY, data })
			},	
		})
	)

  mutate()

  onDone(({data}) => {
		user.$patch({points: data.deleteRedeem.userpoints})
		toast.$patch({message: 'Points were added back to user', color: 'success', open: true})
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
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}
th {
	font-weight: 600;
}
</style>