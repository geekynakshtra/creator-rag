"use client"

import { useState } from "react"
interface Props {
  onAnalyze: (
    videoUrlA: string,
    videoUrlB: string
  ) => void
}

export default function VideoInput({
  onAnalyze
}: Props) {

  const [videoA, setVideoA] =
    useState("")

  const [videoB, setVideoB] =
    useState("")

  return (

    <div className="bg-zinc-900 p-6 rounded-2xl space-y-4">

      <h1 className="text-3xl font-bold">
        Creator RAG Analyzer
      </h1>

      <input
        type="text"
        value={videoA}
        onChange={(e) =>
          setVideoA(e.target.value)
        }
        placeholder="Enter YouTube URL"
        className="w-full p-4 rounded-xl bg-zinc-800"
      />

      <input
        type="text"
        value={videoB}
        onChange={(e) =>
          setVideoB(e.target.value)
        }
        placeholder="Enter Instagram Reel or YouTube URL"
        className="w-full p-4 rounded-xl bg-zinc-800"
      />

      <button
        onClick={() =>
          onAnalyze(videoA, videoB)
        }
        className="bg-white text-black px-6 py-3 rounded-xl font-semibold"
      >
        Analyze Videos
      </button>

    </div>
  )
}