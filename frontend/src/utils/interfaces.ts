export interface UpdatePostVariables {
  id?: number,
  file?: File | null | undefined,
  description?: string
}

interface PostFileType {
  file: string,
  files: {
    lg: string,
    md: string,
    og: string
  },
  width: number,
  height: number
}

export interface PostType {
  id: number,
  description: string,
  postfileSet: PostFileType[],
  likes: number,
  category: {
    id: string,
    oftype: string
  }
}

export interface CompetitionType {
  id: string,
  name: string,
  category: {
    id: string
  },
  description: string,
  lastDate: string,
  points: string,
  image: string,
  expired: boolean,
  message: string
}

export interface CategoryType {
  id: string,
  name: string,
  description: string,
  key: string,
  image: string,
  oftype: string,
  count: string,
  color: string,
  competitions: CompetitionType[],
}

export interface EntityType {
  id: string,
  name: string,
  description: string,
  image: string,
  city: string,
  type: string,
  userAccess: string,
  ispublic: boolean,
  stats: {
    users: number,
    posts: number,
  }
}

export interface EntityDetailsType extends EntityType {
  instagram: '',
  linkedin: '',
  facebook: '',
  stats: {
    users: number,
    posts: number,
    categories: CategoryType[]
  },
  competitions: CompetitionType[]
}

export interface WinnerType {
  post: PostType,
  position: number,
  wonByLikes: number
}

export type TabSelectedType = 'allposts' | 'trending' | 'winners'