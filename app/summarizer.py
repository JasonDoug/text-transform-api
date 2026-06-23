from app.prompts import build_summary_prompt
from app.settings import get_transformation_settings
from app.transformer import LiteLLMTextTransformer, TransformationRequest


_transformer = LiteLLMTextTransformer(get_transformation_settings())


async def summarize_text(text: str, options) -> str:
    prompt = build_summary_prompt(
        text=text,
        length=options.length,
        output_format=options.format,
    )

    result = await _transformer.transform(
        TransformationRequest(
            text=text,
            prompt=prompt,
            include_source_text=False,
        )
    )

    return result.text
