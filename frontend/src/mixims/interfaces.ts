export interface updatePostVariables {
  id?: number,
  file?: string,
  description?: string
}

interface PostFileType {
  file: string
}

export interface Post {
  id: number,
  description: string,
  postfileSet: PostFileType[]
}