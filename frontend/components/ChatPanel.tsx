"use client"

import { useState } from "react"

import { ChatResponse } from "@/types"

import SourceCard from "./SourceCard"

export default function ChatPanel() {
  const [query, setQuery] = useState("")
  const [response, setResponse] = useState<ChatResponse | null>(null)
  const [streamedText, setStreamedText] = useState("")
  const [loading, setLoading] = useState(false)

  const handleAsk = async (
    customQuery?: string
  ) => {
    const finalQuery =
      typeof customQuery === "string"
        ? customQuery
        : query

    if (!finalQuery.trim()) return

    try {
      setLoading(true)
      setStreamedText("")
      setResponse(null)

      const res = await fetch(
        "http://localhost:8000/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: finalQuery
          })
        }
      )

      if (!res.body) {
        throw new Error("No response body")
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()

      let buffer = ""
      let fullAnswer = ""
      let sources: any[] = []

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        buffer += decoder.decode(value, {
          stream: true
        })

        const events = buffer.split("\n\n")

        buffer = events.pop() || ""

        for (const event of events) {
          if (!event.startsWith("data:")) {
            continue
          }

          const jsonText = event
            .replace(/^data:\s*/, "")
            .trim()

          if (!jsonText) {
            continue
          }

          try {
            const parsed = JSON.parse(jsonText)

            if (parsed.type === "sources") {
              sources = parsed.content || []

              setResponse({
                query: finalQuery,
                answer: fullAnswer,
                sources
              })
            }

            if (parsed.type === "token") {
              fullAnswer += parsed.content || ""

              setStreamedText(fullAnswer)

              setResponse({
                query: finalQuery,
                answer: fullAnswer,
                sources
              })
            }
          } catch (error) {
            buffer = `${event}\n\n${buffer}`
            break
          }
        }
      }
    } catch (error) {
      console.error(error)
      alert("Chat streaming failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-zinc-900 p-6 rounded-2xl space-y-6">
      <h2 className="text-2xl font-bold">
        AI Video Analysis Chat
      </h2>

      <div className="flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about the videos..."
          className="flex-1 p-3 rounded-xl bg-zinc-800"
        />

        <button
          onClick={() => handleAsk()}
          disabled={loading}
          className="bg-white text-black px-5 rounded-xl font-semibold disabled:opacity-50"
        >
          {loading ? "Asking..." : "Ask"}
        </button>
      </div>

      {loading && (
        <p className="text-zinc-400">
          Thinking...
        </p>
      )}

      {response && (
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-lg mb-2">
              AI Answer
            </h3>

            <p className="text-zinc-300 whitespace-pre-wrap">
              {streamedText}
            </p>
          </div>

          {response.sources?.length > 0 && (
            <div>
              <h3 className="font-bold text-lg mb-3">
                Sources
              </h3>

              <div className="space-y-3">
                {response.sources.map((source, i) => (
                  <SourceCard
                    key={i}
                    source={source}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}