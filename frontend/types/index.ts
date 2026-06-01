export interface VideoData {
  video_id: string

  platform: string

  title: string

  creator: string

  views: number

  likes: number

  comments: number

  duration: number
  follower_count: number
  upload_date: string

  hashtags: string[]

  transcript: string

  engagement_rate: number

  estimated_views?: boolean

  data_quality_warning?: boolean

  transcript_warning?: boolean
}

export interface SourceChunk {
  score: number

  text: string

  video_id: string

  title: string

  creator: string

  chunk_index: number

  platform: string

  comparison_label?: string

  views?: number

  likes?: number

  comments?: number

  engagement_rate?: number

  duration?: number

  follower_count?: number
}

export interface ChatResponse {
  query: string

  answer: string

  sources: SourceChunk[]
}