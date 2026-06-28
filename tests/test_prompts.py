from app.prompts import (
    build_executive_brief_prompt,
    build_explainer_prompt,
    build_lecture_prompt,
    build_podcast_prompt,
    build_rewrite_prompt,
    build_study_guide_prompt,
    build_translation_prompt,
    build_youtube_short_prompt,
)


def test_build_podcast_prompt_includes_options_and_source_text():
    prompt = build_podcast_prompt(
        text="FastAPI makes APIs simple.",
        length="short",
        output_format="json",
        tone="friendly",
    )

    assert "Transformation type: podcast script" in prompt
    assert "Podcast length: short" in prompt
    assert "Output format: json" in prompt
    assert "Tone: friendly" in prompt
    assert "two-host podcast script" in prompt
    assert "valid JSON" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_explainer_prompt_includes_options_and_source_text():
    prompt = build_explainer_prompt(
        text="FastAPI makes APIs simple.",
        length="medium",
        output_format="plain",
        tone="professional",
    )

    assert "Transformation type: explainer" in prompt
    assert "Explainer length: medium" in prompt
    assert "Output format: plain" in prompt
    assert "Tone: professional" in prompt
    assert "beginner-friendly explainer" in prompt
    assert "simple language" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_lecture_prompt_includes_options_and_source_text():
    prompt = build_lecture_prompt(
        text="FastAPI makes APIs simple.",
        length="long",
        output_format="plain",
        tone="professional",
    )

    assert "Transformation type: lecture" in prompt
    assert "Lecture length: long" in prompt
    assert "learning objectives" in prompt
    assert "key takeaways" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_study_guide_prompt_includes_options_and_source_text():
    prompt = build_study_guide_prompt(
        text="FastAPI makes APIs simple.",
        length="medium",
        output_format="plain",
        tone="friendly",
    )

    assert "Transformation type: study guide" in prompt
    assert "Study guide length: medium" in prompt
    assert "key terms" in prompt
    assert "review questions" in prompt
    assert "short quiz" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_executive_brief_prompt_includes_options_and_source_text():
    prompt = build_executive_brief_prompt(
        text="FastAPI makes APIs simple.",
        length="short",
        output_format="plain",
        tone="professional",
    )

    assert "Transformation type: executive brief" in prompt
    assert "Executive brief length: short" in prompt
    assert "main point" in prompt
    assert "business implications" in prompt
    assert "recommended next step" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_rewrite_prompt_includes_options_and_source_text():
    prompt = build_rewrite_prompt(
        text="FastAPI makes APIs simple.",
        length="medium",
        output_format="plain",
        tone="friendly",
    )

    assert "Transformation type: rewrite" in prompt
    assert "Rewrite length: medium" in prompt
    assert "Output format: plain" in prompt
    assert "Tone: friendly" in prompt
    assert "rewritten version" in prompt
    assert "Improve clarity, flow, and readability" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_translation_prompt_includes_options_and_source_text():
    prompt = build_translation_prompt(
        text="FastAPI makes APIs simple.",
        length="short",
        output_format="plain",
        tone="professional",
    )

    assert "Transformation type: translation" in prompt
    assert "Translation length: short" in prompt
    assert "Output format: plain" in prompt
    assert "Tone: professional" in prompt
    assert "translation" in prompt
    assert "Preserve the original meaning and nuance" in prompt
    assert "FastAPI makes APIs simple." in prompt


def test_build_youtube_short_prompt_includes_options_and_source_text():
    prompt = build_youtube_short_prompt(
        text="FastAPI makes APIs simple.",
        length="medium",
        output_format="plain",
        tone="professional",
    )

    assert "Transformation type: YouTube Short script" in prompt
    assert "YouTube Short length: medium" in prompt
    assert "Output format: plain" in prompt
    assert "Tone: professional" in prompt
    assert "high-retention script" in prompt
    assert "strong, curiosity-inducing hook" in prompt
    assert "FastAPI makes APIs simple." in prompt

