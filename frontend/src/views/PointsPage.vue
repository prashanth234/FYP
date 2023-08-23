<template>
	<ion-page>
		<ion-content class="ion-padding">
			<h1>{{`hello ${user.username}, you have ${user.points} points`}}</h1>

			<ion-row>

				<ion-col size="6">
					<ion-input v-model="state.points" label="Points" type="number" placeholder="000"></ion-input>
				</ion-col>
				
				<ion-col size="6">
					<ion-button @click="createReedem">Submit</ion-button>
					<ion-button @click="UpdateReedem">Update</ion-button>
					<ion-button @click="DeleteReedem">Delete</ion-button>
				</ion-col>

				<ion-col cols="6" v-for="(redemption, index) in redemptions?.redemptions" :key="redemption">
					{{ `status = ${redemption.status} | createdAt = ${redemption.createdAt} | points = ${redemption.points}`  }}
				</ion-col>

			</ion-row>

		</ion-content>
	</ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonContent, IonRow, IonCol, IonInput, IonButton } from '@ionic/vue';
import { useUserStore } from '@/stores/user';
import gql from 'graphql-tag'
import { useQuery, useMutation } from '@vue/apollo-composable'
import { reactive } from 'vue';

const user = useUserStore()

const state = reactive({
	points: ''
})

const { result: redemptions, onResult } = useQuery(gql`
                              query {
                                redemptions {
                                  status,
																	points,
																	createdAt
                                }
                              }
                            `)

onResult(({data, loading}) => {
	console.log(data)
})

function createReedem () {
	const { mutate, onDone, error, onError } = useMutation(gql`    
    
    mutation ($points: Int!) { 
      createRedeem (
        points: $points,
      ) {
          redeem {
						points,
						status
					} 
        }
    }

  `, {
		variables: {points: parseInt(state.points)}	
	})

  mutate()

  onDone(() => {
  })

  onError((error: any) => {
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

function DeleteReedem () {

}


</script>