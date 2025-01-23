"""Utility functions for reuse."""

import textract
from openai import AsyncOpenAI

from api.settings import settings


def extract_file_content(file_path: str) -> str:
    """Function for extracting content from a file."""
    try:
        content = textract.process(file_path).decode("utf-8")
        return content
    except Exception as e:
        raise e


async def get_summary_from_openai(content: str) -> str:
    """Function for requesting content summary from ChatGPT."""
    client = AsyncOpenAI(
        api_key=settings.CHATGPT_API_KEY,
    )

    # Generate summary with ChatGPT
    try:
        summary_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes documents.",
                },
                {"role": "user", "content": f"Summarize this document:\n{content[:4000]}"},
            ],
        )
        summary = summary_response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        raise e
