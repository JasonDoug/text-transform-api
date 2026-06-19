from app.schemas import SummaryFormat, SummaryLength


def build_summary_prompt(text: str, length: SummaryLength | str, output_format: SummaryFormat | str) -> str:
    length_value = length.value if isinstance(length, SummaryLength) else length
    format_value = output_format.value if isinstance(output_format, SummaryFormat) else output_format

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
