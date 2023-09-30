/* Graphql */
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context'
import { createUploadLink } from "apollo-upload-client"

// HTTP connection to the API
const httpLink = createUploadLink({
  // You should use an absolute URL here
  uri: `${import.meta.env.VITE_APP_BASE_URL}/graphql`,
})

// create auth link
const authLink = setContext((_, { headers }) => {
  // get the authentication token from local storage if it exists
  const token = localStorage.getItem('fyptoken');

  // return the headers to the context so that httpLink can read them
  return {
    headers: {
      ...headers,
      authorization: token ? `JWT ${token}` : ''
    }
  };
});

// Cache implementation
const cache = new InMemoryCache({
  typePolicies: {
    UserNode: {
      keyFields: ['username']
    }
  }
})

// Create the apollo client
const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache,
})

// For Options API
// import { createApolloProvider } from '@vue/apollo-option'

// const apolloProvider = createApolloProvider({
//   defaultClient: apolloClient,
// })

export { apolloClient }