from json import JSONDecodeError
from typing import Any, Dict

import httpx

from app.core.config import settings
from app.exceptions import (
    QuestionIncorrectStructureError,
    QuestionLenError,
    QuestionRequestError,
)
from app.schemas import ManyQuestionParseShema
from pydantic import ValidationError

REQUEST_HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}


def get_jservice_query_params(questions_num: int) -> Dict[str, Any]:
    return {"count": questions_num}


async def parse_jservice_random_questions(
    questions_num: int,
) -> ManyQuestionParseShema:
    """Возвращает с хостинга https://jservice.io распарсиные данные."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.JSERVICE_URL,
                headers=REQUEST_HEADERS,
                params=get_jservice_query_params(questions_num),
            )
            response.raise_for_status()
            if len(results := response.json()) < questions_num:
                raise QuestionLenError
            print(results)
            return ManyQuestionParseShema(results=results)
    except httpx.HTTPError as exc:
        raise QuestionRequestError(
            settings.JSERVICE_URL, questions_num
        ) from exc
    except (JSONDecodeError, KeyError, TypeError, ValidationError) as exc:
        raise QuestionIncorrectStructureError(
            settings.JSERVICE_URL, questions_num
        ) from exc
