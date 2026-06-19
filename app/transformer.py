from __future__ import annotations

import asyncio
from dataclasses import dataclass

import litellm

from app.settings import TransformationSettings


@dataclass(frozen=True)
class TransformationRequest:
    text: str
    prompt: str


@dataclass(frozen=True)
class TransformationResult:
    text: str
    provider: str
    model: str


class LiteLLMTextTransformer:
    def __init__(self, settings: TransformationSettings):
        self.settings = settings

    async def transform(self, request: TransformationRequest) -> TransformationResult:
        response = await asyncio.to_thread(
            litellm.completion,
            model=self._model_name(),
            api_base=self.settings.base_url,
            api_key=self.settings.api_key,
            messages=[
                {
                    "role": "system",
                    "content": "You are a text transformation engine. Follow the user's transformation instructions exactly. Return only the transformed text unless the user explicitly asks for JSON or another structured format.",
                },
                {
                    "role": "user",
                    "content": request.prompt,
                },
            ],
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            timeout=self.settings.timeout,
        )

        return TransformationResult(
            text=response.choices[0].message.content.strip(),
            provider=self.settings.provider,
            model=self.settings.model,
        )

    def _model_name(self) -> str:
        if self.settings.provider == "openai-compatible" and not self.settings.model.startswith("openai/"):
            return f"openai/{self.settings.model}"

        return self.settings.model
