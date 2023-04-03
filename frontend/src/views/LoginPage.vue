<template>
    <h1>hello</h1>
    <div>{{  allCategories }}</div>
</template>

<script>
import gql from 'graphql-tag'

export default {
    apollo: {
        allCategories: gql`query {
                    allCategories {
                        name
                    }
                }`,
    },
    data () {
        return { 
            allCategories: []
        }
    },
    methods: {
        // async getdata () {
        //     let data = await this.$apolloClient.query({
        //         query: gql `
        //             query allCategories {
        //                 name
        //             }
        //         `
        //     })
        //     console.log(data)
        // }
    },
    mounted () {
        // this.getdata()
        setTimeout(() => {
            console.log(this.allCategories)
        }, 4000);
    }
}
</script>