
import gql from 'graphql-tag'

export function getQuery() {
  const QUERY = gql`
									query CoinActivities {
										coinactivities {
											id,
											points,
											description,
											status,
											createdAt,
											comments
										}
									}
								`
  return QUERY
}

export interface CoinActivity {
  id: string,
  points: number,
  description: string,
  status: string,
  createdAt: string
}

export interface CoinActivities {
  coinactivities: CoinActivity[]
}