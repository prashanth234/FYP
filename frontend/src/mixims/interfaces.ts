export interface UpdatePostVariables {
  id?: number,
  file?: File | null | undefined,
  description?: string
}

interface PostFileType {
  file: string
}

export interface Post {
  id: number,
  description: string,
  postfileSet: PostFileType[],
  category: {
    oftype: string
  }
}

export interface CompetitionInfo {
  id: string,
  name: string,
  description: string,
  lastDate: string,
  points: number,
  image: string,
  expired: boolean
}

export interface categoryObject {
  name: string,
  description: string,
  type: string,
  id: string,
  image: string,
  oftype: string
}