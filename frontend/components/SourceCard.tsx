import { SourceChunk } from "@/types"

interface Props {
  source: SourceChunk
}

export default function SourceCard({
  source
}: Props) {

  return (
    <div className="bg-zinc-800 p-4 rounded-xl space-y-3 border border-zinc-700">

      <div className="flex flex-wrap items-center gap-2 text-xs">

        <span className="bg-white text-black px-2 py-1 rounded-full font-semibold">
          Video {source.comparison_label || "?"}
        </span>

        <span className="bg-zinc-700 px-2 py-1 rounded-full uppercase">
          {source.platform}
        </span>

        <span className="bg-zinc-700 px-2 py-1 rounded-full">
          Chunk #{source.chunk_index}
        </span>

      </div>

      <div>

        <p className="font-semibold text-sm">
          {source.title}
        </p>

        <p className="text-zinc-400 text-xs">
          Creator: {source.creator}
        </p>

      </div>

      <p className="text-zinc-300 text-sm whitespace-pre-wrap leading-6">
        {source.text}
      </p>

    </div>
  )
}