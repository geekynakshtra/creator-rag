"use client"

import { useState } from "react"
import VideoInput from "@/components/VideoInput"
import VideoCard from "@/components/VideoCard"
import ChatPanel from "@/components/ChatPanel"
import api from "@/services/api"
import { VideoData } from "@/types"

export default function Home() {
  const [videoA, setVideoA] = useState<VideoData | null>(null)
  const [videoB, setVideoB] = useState<VideoData | null>(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (
    videoUrlA: string,
    videoUrlB: string
  ) => {
    try {
      setLoading(true)

      const responseA = await api.post
      ( "/ingest/video",
          {
              url: videoUrlA,
              comparison_label: "A"
          }
      )
      setVideoA(responseA.data)

      const responseB = await api.post
      ("/ingest/video",
          {
              url: videoUrlB,
              comparison_label: "B"
          }
      )
      setVideoB(responseB.data)

    } catch (error) {
      console.error(error)
      alert("Failed to analyze videos")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <div className="max-w-6xl mx-auto space-y-8">

        <VideoInput onAnalyze={handleAnalyze} />

        {loading && (
          <p className="text-zinc-400">
            Analyzing videos...
          </p>
        )}

        {videoA && videoB && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <VideoCard video={videoA} />
            <VideoCard video={videoB} />
          </div>
        )}

        {videoA && videoB && (
          <ChatPanel />
        )}

      </div>
    </main>
  )
}
