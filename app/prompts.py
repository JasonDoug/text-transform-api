from app.schemas import SummaryFormat, SummaryLength


def build_summary_prompt(text: str, length: SummaryLength | str, output_format: SummaryFormat | str) -> str:
    length_value = length.value if isinstance(length, SummaryLength) else length
    format_value = output_format.value if isinstance(output_format, SummaryFormat) else str(output_format)

    format_instruction = "Return the summary as bullet points." if format_value == "bullets" else "Return the summary as a single paragraph."

    return f"""You are a text transformation engine.

Transformation type: summary
Summary length: {length_value}
Output format: {format_value}

Instructions:
- Transform the provided text into a useful summary.
- Preserve the most important facts and meaning.
- Do not invent details that are not in the source text.
- Return only the transformed text.
- {format_instruction}

Source text:
{text}
"""


def build_podcast_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="podcast script",
        label="Podcast length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a two-host podcast script.",
        instructions=[
            "Make the script engaging and easy to follow.",
            "Use two distinct hosts.",
            "Preserve the facts from the source text.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_explainer_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="explainer",
        label="Explainer length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a beginner-friendly explainer.",
        instructions=[
            "Use simple language.",
            "Explain the core idea clearly.",
            "Include one concrete example when useful.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_lecture_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="lecture",
        label="Lecture length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a short lecture.",
        instructions=[
            "Include learning objectives.",
            "Explain the topic in a structured teaching style.",
            "Include examples that help a learner understand the topic.",
            "End with key takeaways.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_study_guide_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="study guide",
        label="Study guide length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a study guide.",
        instructions=[
            "Include key terms.",
            "Include review questions.",
            "Include a short quiz with answers.",
            "Organize the guide so a learner can study from it.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_executive_brief_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="executive brief",
        label="Executive brief length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a concise executive brief.",
        instructions=[
            "Start with the main point.",
            "Explain business implications.",
            "Include risks, opportunities, or tradeoffs when relevant.",
            "End with a recommended next step.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_rewrite_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="rewrite",
        label="Rewrite length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a rewritten version.",
        instructions=[
            "Preserve the original meaning and facts.",
            "Improve clarity, flow, and readability.",
            "Adjust the tone as specified.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_translation_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="translation",
        label="Translation length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into a translation.",
        instructions=[
            "Translate accurately to the target language implied by tone.",
            "Preserve the original meaning and nuance.",
            "Maintain the specified tone in the translation.",
            "Do not invent details that are not in the source text.",
        ],
    )


def build_youtube_short_prompt(text: str, length: str, output_format: str, tone: str) -> str:
    return _build_named_prompt(
        transformation_type="YouTube Short script",
        label="YouTube Short length",
        text=text,
        length=length,
        output_format=output_format,
        tone=tone,
        purpose="Transform the provided text into an engaging, high-retention script for a vertical YouTube Short or TikTok video.",
        instructions=[
            "Start with a strong, curiosity-inducing hook in the first 3 seconds.",
            "Deliver information quickly with high pacing and concise sentences.",
            "Include visual cues in brackets, e.g. [Show close-up of phone], to guide editing.",
            "End with a loop hook or a clear call to action (like 'subscribe' or 'comment below').",
            "Do not invent details that are not in the source text.",
        ],
    )



def _build_named_prompt(
    transformation_type: str,
    label: str,
    text: str,
    length: str,
    output_format: str,
    tone: str,
    purpose: str,
    instructions: list[str],
) -> str:
    return f"""You are a text transformation engine.

Transformation type: {transformation_type}
{label}: {length}
Output format: {output_format}
Tone: {tone}

Instructions:
- {purpose}
{_format_instructions(instructions)}
- {_format_instruction(output_format)}

Source text:
{text}
"""


def _format_instructions(instructions: list[str]) -> str:
    return "\n".join(f"- {instruction}" for instruction in instructions)


def _format_instruction(output_format: str) -> str:
    if output_format == "json":
        return "Return valid JSON only. Do not wrap the response in markdown. Do not include explanatory text outside the JSON."

    return "Return only the transformed text. Do not include explanatory text outside the transformation."
