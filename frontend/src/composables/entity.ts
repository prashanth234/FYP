import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

export function useJoinEntityAPI() {

  const { mutate, onDone, onError } = useMutation(gql`    
    
    mutation joinEntity ($file: Upload, $code: String, $entityId: ID!) { 
      joinEntity (
        file: $file,
        code: $code,
        entityId: $entityId
      ) {
          success,
          message,
          entity {
            id,
            userAccess,
            stats {
              id,
              users
            }
          }
        }
    }

  `, () => ({
      variables: {}
    })

  )

  return {
    mutate,
    onDone,
    onError
  }

}