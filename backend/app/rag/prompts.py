def build_rag_prompt(
    query,
    chunks,
    memory_context="",
    mode="general_analysis",
    metadata_summary=""
):


# BUILD CONTEXT

    context = "\n\n".join([

        f"""
VIDEO {chunk.get('comparison_label')}

TITLE:
{chunk.get('title')}

CREATOR:
{chunk.get('creator')}

PLATFORM:
{chunk.get('platform')}

VIEWS:
{chunk.get('views')}

LIKES:
{chunk.get('likes')}

COMMENTS:
{chunk.get('comments')}

ENGAGEMENT RATE:
{chunk.get('engagement_rate')}%

FOLLOWERS:
{chunk.get('follower_count')}

DURATION:
{chunk.get('duration')} seconds

CHUNK INDEX:
{chunk.get('chunk_index')}

TRANSCRIPT:
{chunk.get('text')}
"""

        for chunk in chunks
    ])


# BASE RULES

    base_rules = """
You are an AI creator analyst.

You are comparing VIDEO A and VIDEO B.

STRICT RULES:
- Use ONLY provided transcript and metadata context.
- NEVER invent visuals.
- NEVER invent emotions.
- NEVER invent editing.
- NEVER invent pacing unless transcript supports it.
- NEVER invent audience demographics.
- NEVER hallucinate creators or metrics.
- NEVER estimate follower count.
- NEVER mention chunk numbers that do not exist.
- NEVER reference evidence not explicitly retrieved.
- If transcript evidence is weak or missing, say:
  "Not enough transcript evidence available."
- When making a claim, mention the source as:
  "(Video A, Chunk #0)" or "(Video B, Chunk #0)".
- Every comparison point should identify whether it came from Video A or Video B.

FOLLOWER COUNT RULES:
- Follower count is metadata, not transcript evidence.
- If follower_count is 0, None, missing, or unavailable, say exactly:
  "Follower count data unavailable from platform metadata."
- Do NOT say "Not enough transcript evidence available" for follower count.
- Do NOT say "Not enough metadata evidence available" for follower count.
- Do NOT estimate follower count.

IMPORTANT:
- Only use retrieved metadata values.
- Only use retrieved transcript text.
- Do NOT speculate.
- Do NOT infer hidden analytics.
- Do NOT create fake comparisons.
- Keep answers concise.
- Use bullet points.
"""

# MODE: HOOK ANALYSIS

    if mode == "hook_analysis":

        instructions = """
Focus on:
- first impressions
- curiosity hooks
- emotional triggers
- opening statements
- retention potential based only on available hook text

Only analyze transcript evidence from opening chunks.
"""


# MODE: ENGAGEMENT ANALYSIS

    elif mode == "engagement_analysis":

        instructions = """
Focus on:
- engagement rate differences
- title effectiveness
- creator reach
- platform differences
- transcript style differences

You may make LIGHT analytical inferences ONLY if directly supported by metadata or transcript evidence.

Do NOT invent:
- visuals
- editing
- pacing
- audience demographics
- emotions

If evidence is weak, clearly say:
"Limited transcript evidence available."
"""


# MODE: IMPROVEMENT ANALYSIS

    elif mode == "improvement_analysis":

        instructions = """
You are a creator improvement analyst.

IMPORTANT:
- Follow the user's requested direction.
- If the user asks "improve B based on A", then VIDEO A is the reference and VIDEO B is the target.
- If the user asks "improve A based on B", then VIDEO B is the reference and VIDEO A is the target.
- Do NOT reverse the requested direction.
- Always name the reference video and target video clearly.

Rules:
- First identify what the reference video did well.
- Then explain how the target video can adapt that strength.
- If the target video already has a strength, say it should keep it.
- Do NOT confuse VIDEO A and VIDEO B.
- Do NOT treat full video duration as hook duration.
- Do NOT invent visuals, editing, audience, or emotions.
- Every suggestion must cite source like:
  (Video A, Chunk #0) or (Video B, Chunk #0)

Preferred format:
- Strength from reference video:
- Improvement for target video:
- Evidence:
"""


# MODE: CREATOR ANALYSIS

    elif mode == "creator_analysis":

        instructions = """
You are an information extraction system.

ONLY extract:
- creator name
- platform
- follower count
- views
- likes
- comments
- engagement rate

If follower_count is 0, None, missing, or unavailable, say exactly:
"Follower count data unavailable from platform metadata."

Do NOT infer.
Do NOT guess.
Do NOT estimate follower count.
Do NOT use transcript evidence for follower count.
"""


# DEFAULT MODE

    else:

        instructions = """
Provide a grounded comparison using only retrieved evidence.
"""


# FINAL PROMPT

    prompt = f"""
{base_rules}

{instructions}

Conversation History:
{memory_context}

User Question:
{query}

VIDEO METADATA:
{metadata_summary}

Retrieved Context:
{context}

Answer:
"""

    return prompt