<template>

  <div class="grid-container" v-if="requests?.joinRequests.length">

    <div
      class="grid-item cpointer"
      v-for="(request, index) in requests.joinRequests"
      :key="index"
    >

      <UserCard :user="request.user" :files="request.files" @action="approveRequest(request.id, $event)">
      </UserCard>

    </div>

  </div>

  <div v-else class="ion-text-center ion-margin no-items">
    No Pendings Requests
  </div>

</template>

<script lang="ts" setup>
import gql from 'graphql-tag'
import { useMutation, useQuery } from "@vue/apollo-composable"
import UserCard from '@/components/UserCardContainer.vue'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
  entityId: String
})

const toast = useToastStore();

const JOIN_REQUEST_QUERY = gql `
  query JoinRequests ($entity_id: ID!) {
    joinRequests(entityId: $entity_id) {
      files,
      id,
      user {
        id,
        username,
        avatar
      }
    }
  }
`
const { result: requests } = useQuery(JOIN_REQUEST_QUERY, () => ({
  entity_id: props.entityId
}))

function approveRequest(verificationId: string, approve: Boolean) {

  const APPROVE_REQ_MUTATION = gql `
    mutation ApproveJoinRequest ($verificationId: ID!, $approve: Boolean!) {
      approveJoinRequest (verificationId: $verificationId, approve: $approve) {
        success
      }
    }
  `

  const { mutate, onDone, onError } = useMutation(APPROVE_REQ_MUTATION, () => ({
    variables: {
      verificationId: verificationId,
      approve
    },
    update: (cache, { data: { } }) => {
      const normalizedVerfId = cache.identify({ id: verificationId, __typename: 'JoinRequestType' });
      cache.evict({ id: normalizedVerfId })
      cache.gc()
    }
  }))

  mutate()

  onDone(({data}) => {
    if (data.approveJoinRequest.success && approve) {
      toast.$patch({message: 'User added to entity.', color: 'success', open: true})
    }
  })
}

</script>

<style lang="scss" scoped>

.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
	grid-gap: 20px;
	/* Ensure all rows have the same height */
	grid-auto-rows: auto;
}

.grid-item {
	color: var(--ion-text-color);
	display: flex;
	flex-direction: column;
	text-align: center;
}

.no-items {
  font-size: 18x;
  font-weight: 500;
}
</style>