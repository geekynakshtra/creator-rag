import { VideoData } from "@/types"

interface Props {
  video: VideoData
}

const safeNumber = (val?: number) => val ?? 0

const formatUploadDate = (date?: string) => {
  if (!date) return "Unavailable"

  if (date.length === 8) {
    return `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`
  }

  return date
}

export default function VideoCard({ video }: Props) {
  return (
    <div className="bg-zinc-900 p-6 rounded-2xl space-y-4">

      <div className="flex items-center justify-between">
        <span className="text-xs uppercase bg-zinc-800 px-3 py-1 rounded-full">
          {video.platform}
        </span>

        <span className="text-green-400 font-semibold">
          {video.engagement_rate
            ? `${video.engagement_rate}% ER`
            : "ER unavailable"}
        </span>
      </div>

      <h2 className="text-xl font-bold">
        {video.title}
      </h2>

      <div className="space-y-1">
        <p className="text-zinc-400">
          Creator: {video.creator}
        </p>

        <p className="text-zinc-400">
          Followers:{" "}
          {video.follower_count && video.follower_count > 0
            ? video.follower_count.toLocaleString()
            : "Unavailable"}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">

        <div className="bg-zinc-800 p-3 rounded-xl">
          <p className="text-zinc-400">Views</p>
          <p>{safeNumber(video.views).toLocaleString()}</p>
        </div>

        <div className="bg-zinc-800 p-3 rounded-xl">
          <p className="text-zinc-400">Likes</p>
          <p>{safeNumber(video.likes).toLocaleString()}</p>
        </div>

        <div className="bg-zinc-800 p-3 rounded-xl">
          <p className="text-zinc-400">Comments</p>
          <p>{safeNumber(video.comments).toLocaleString()}</p>
        </div>

        <div className="bg-zinc-800 p-3 rounded-xl">
          <p className="text-zinc-400">Duration</p>
          <p>{safeNumber(video.duration)}s</p>
        </div>

        <div className="bg-zinc-800 p-3 rounded-xl col-span-2">
          <p className="text-zinc-400">Upload Date</p>
          <p>{formatUploadDate(video.upload_date)}</p>
        </div>

      </div>

      <div>
        <p className="text-zinc-400 mb-2">
          Hashtags
        </p>

        <div className="flex flex-wrap gap-2">
          {video.hashtags?.length ? (
            video.hashtags.slice(0, 8).map((tag, i) => (
              <span
                key={i}
                className="bg-zinc-800 px-2 py-1 rounded-lg text-xs"
              >
                #{tag}
              </span>
            ))
          ) : (
            <p className="text-zinc-500 text-sm">
              No hashtags found
            </p>
          )}
        </div>
      </div>

    </div>
  )
}