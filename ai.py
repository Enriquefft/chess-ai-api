"""OpenAI API client for chat completions."""

from typing import TYPE_CHECKING

from openai import OpenAI

if TYPE_CHECKING:
    from openai.types.chat import (
        ChatCompletionMessageParam,
        ChatCompletionSystemMessageParam,
    )

from typing import Optional

from env import OPENAI_API_KEY

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def get_response(
    user_message: str,
    system_message: Optional[str] = None,
) -> Optional[str]:
    """Get a response from the OpenAI API."""
    user_role_message: ChatCompletionMessageParam = {
        "role": "user",
        "content": user_message,
    }
    system_role_message: ChatCompletionSystemMessageParam | None = (
        {"role": "system", "content": system_message} if system_message else None
    )

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        # messages=[system_role_message (if not None), user_role_message],
        messages=[system_role_message, user_role_message]
        if system_role_message
        else [user_role_message],
    )
    return completion.choices[0].message.content
