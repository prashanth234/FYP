/* Graphql */
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { createUploadLink } from "apollo-upload-client";

// HTTP connection to the API
const httpLink = createUploadLink({
  // You should use an absolute URL here
  uri: 'http://localhost:8000/graphql',
})

// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
const apolloClient = new ApolloClient({
  link: httpLink,
  cache,
})

// For Options API
// import { createApolloProvider } from '@vue/apollo-option'

// const apolloProvider = createApolloProvider({
//   defaultClient: apolloClient,
// })

export { apolloClient }