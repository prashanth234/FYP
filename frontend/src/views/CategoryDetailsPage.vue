<template>
  <ion-content style="height: 100%;">
    
    hello

  </ion-content>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

const { result } = useQuery(gql`
                              query ($id: Int!) {
                                categoryDetails (id: $id) {
                                  name
                                }
                              }
                            `)


watch(result, value => {
      console.log(value)
    })


</script>

<!-- <script>
import gql from 'graphql-tag'

export default {
  apollo: {
      categories: gql`query {
                            categories {
                                name,
                                description,
                                type,
                                id
                            }
                        }`,
  },
  data () {
      return { 
        categories: []
      }
  },
  methods: {
  },
  mounted () {
  }
}
</script> -->