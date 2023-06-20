export interface updatePostVariables {
  id?: number,
  file?: File | null,
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