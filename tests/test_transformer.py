import os

import pytest

from app.prompts import build_summary_prompt
from app.settings import TransformationSettings
from app.transformer import LiteLLMTextTransformer, TransformationRequest, TransformationResult


class FakeChoice:
    def __init__(self, message):
        self.message = message


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeCompletion:
    def __init__(self, content):
        self.choices = [FakeChoice(FakeMessage(content))]


def test_build_summary_prompt_includes_length_and_format(monkeypatch):
    monkeypatch.setenv("TRANSFORMATION_MODEL", "llama3.1:8b")

    prompt = build_summary_prompt(
        text="Alpha. Beta. Gamma.",
        length="medium",
        output_format="bullets",
    )

    assert "Alpha. Beta. Gamma." in prompt
    assert "medium" in prompt
    assert "bullet points" in prompt


def test_transformation_settings_supports_openai_compatible_provider(monkeypatch):
    monkeypatch.setenv("TRANSFORMATION_PROVIDER", "openai-compatible")
    monkeypatch.setenv("TRANSFORMATION_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("TRANSFORMATION_API_KEY", "ollama")
    monkeypatch.setenv("TRANSFORMATION_MODEL", "llama3.1:8b")

    settings = TransformationSettings.from_env()

    assert settings.provider == "openai-compatible"
    assert settings.base_url == "http://localhost:11434/v1"
    assert settings.api_key == "ollama"
    assert settings.model == "llama3.1:8b"


@pytest.mark.asyncio
async def test_litellm_transformer_calls_openai_compatible_endpoint(monkeypatch):
    monkeypatch.setenv("TRANSFORMATION_PROVIDER", "openai-compatible")
    monkeypatch.setenv("TRANSFORMATION_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("TRANSFORMATION_API_KEY", "ollama")
    monkeypatch.setenv("TRANSFORMATION_MODEL", "llama3.1:8b")

    calls = {}

    def fake_completion(**kwargs):
        calls.update(kwargs)
        return FakeCompletion("Generated summary")

    monkeypatch.setattr("litellm.completion", fake_completion)

    transformer = LiteLLMTextTransformer(TransformationSettings.from_env())

    result = await transformer.transform(
        TransformationRequest(
            text="Alpha. Beta. Gamma.",
            prompt="Summarize this text.",
        )
    )

    assert result.text == "Generated summary"
    assert calls["model"] == "openai/llama3.1:8b"
    assert calls["api_base"] == "http://localhost:11434/v1"
    assert calls["api_key"] == "ollama"
    assert calls["messages"][0]["role"] == "system"
    assert calls["messages"][1]["role"] == "user"
