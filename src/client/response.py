"""preferred response class for all API requests"""

__all__ = ["STREAM_FILE_PATH", "ResponseGetData", "find_ip"]

import re
from dataclasses import dataclass, field
from typing import Any, Optional


import httpx
import requests
from bs4 import BeautifulSoup


@dataclass
class RequestMetadata:
    url: str
    headers: dict = field(repr=False, default_factory=dict)
    body: Optional[str] = field(default=None)
    params: Optional[dict] = field(default=None)


@dataclass
class ResponseGetData:
    """preferred response class for all API Requests"""

    status: int
    response: Any
    is_success: bool

    request_metadata: Optional[RequestMetadata] = field(default=None)
    additional_information: Optional[dict] = field(default=None, repr=False)

    @classmethod
    def from_requests_response(
        cls,
        res: requests.Response,  # requests response object
        additional_information: Optional[dict] = None,
        request_metadata: Optional[RequestMetadata] = None,
    ) -> "ResponseGetData":
        """returns ResponseGetData"""

        # JSON responses
        response = None
        if res.ok:
            if "application/json" in res.headers.get("Content-Type", {}):
                response = res.json()

            else:
                response = res.text

            return cls(
                status=res.status_code,
                response=response,
                additional_information=additional_information,
                request_metadata=request_metadata,
                is_success=True,
            )

        # errors
        return cls(
            status=res.status_code,
            response=res.reason,
            additional_information=additional_information,
            request_metadata=request_metadata,
            is_success=False,
        )

    @classmethod
    def from_httpx_response(
        cls,
        res: httpx.Response,  # httpx response object
        request_metadata: Optional[RequestMetadata] = None,
        additional_information: Optional[dict] = None,
    ) -> "ResponseGetData":
        """returns ResponseGetData"""

        # JSON responses
        ok = res.status_code <= 399 and res.status_code >= 200

        body = None
        if hasattr(res.request, "content"):
            body = res.request.content

        # Ensure body is a string or None before passing to ResponseGetData
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        if ok:
            try:
                if "application/json" in res.headers.get("Content-Type", {}):
                    return cls(
                        status=res.status_code,
                        response=res.json(),
                        is_success=True,
                        additional_information=additional_information,
                        request_metadata=request_metadata,
                    )

            except ValueError:
                return cls(
                    status=res.status_code,
                    response=res.text,
                    is_success=True,
                    additional_information=additional_information,
                    request_metadata=request_metadata,
                )

        # errors
        response_text = res.reason_phrase if hasattr(res, "reason_phrase") else "Unknown reason"
        return cls(
            status=res.status_code,
            response=response_text,
            is_success=False,
            request_metadata=request_metadata,
            additional_information=additional_information,
        )

    @classmethod
    async def from_looper(
        cls, res: "ResponseGetData", array: list  # requests response object
    ) -> "ResponseGetData":
        """async method returns ResponseGetData"""

        if not res.is_success:
            return res

        res.response = array
        return res


def find_ip(html, html_tag: str = "p"):
    ip_address_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    soup = BeautifulSoup(html, "html.parser")

    return re.findall(ip_address_regex, str(soup.find(html_tag)))[0]


STREAM_FILE_PATH = "__large-file.json"


async def _write_stream(
    res: httpx.Response, file_name: str = STREAM_FILE_PATH, stream_chunks=10
):
    print(type(res), type(res.content), stream_chunks)

    index = 0
    with open(file_name, "wb") as fd:
        async for chunk in res.aiter_bytes():
            index += 1
            print(f"writing chunk - {index}")
            fd.write(chunk)

    print("done writing stream")

    return None


async def _read_stream(file_name: str):
    with open(file_name, "rb") as f:
        return f.read()
