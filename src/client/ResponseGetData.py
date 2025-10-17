"""preferred response class for all API requests"""


__all__ = ["STREAM_FILE_PATH", "BlockedByVPN", "ResponseGetData", "find_ip"]

import re
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx
import requests
from bs4 import BeautifulSoup
from nbdev.showdoc import patch_to

from . import DomoError as dmde
from . import Logger as dl


class BlockedByVPN(dmde.RouteError):
    def __init__(
        self,
        res,
        ip_address: str = None,
    ):
        ip_address_str = f"from {ip_address}" if ip_address else ""
        message = f"request blocked {ip_address_str} - check VPN settings"

        super().__init__(message=message, res=res)


@dataclass
class ResponseGetData:
    """preferred response class for all API Requests"""

    status: int
    response: Any
    is_success: bool
    auth: dict = field(repr=False, default=None)
    parent_class: str = None
    traceback_details: any = field(default=None, repr=False)
    url: str = None
    body: str = None

    def set_response(self, response):
        self.response = response


@patch_to(ResponseGetData, cls_method=True)
def _from_requests_response(
    cls, res: requests.Response  # requests response object
) -> ResponseGetData:
    """returns ResponseGetData"""

    # JSON responses
    if res.ok and "application/json" in res.headers.get("Content-Type", {}):
        return cls(status=res.status_code, response=res.json(), is_success=True)

    # default text responses
    elif res.ok:
        return cls(status=res.status_code, response=res.text, is_success=True)

    # errors
    return cls(status=res.status_code, response=res.reason, is_success=False)


def find_ip(html, html_tag: str = "p"):
    ip_address_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    soup = BeautifulSoup(html, "html.parser")

    return re.findall(ip_address_regex, str(soup.find(html_tag)))[0]


@patch_to(ResponseGetData, cls_method=True)
def _from_httpx_response(
    cls,
    res: requests.Response,  # requests response object
    auth: Optional[any] = None,
    parent_class: str = None,
    traceback_details: dl.TracebackDetails = None,
) -> ResponseGetData:
    """returns ResponseGetData"""

    # JSON responses

    ok = True if res.status_code <= 399 and res.status_code >= 200 else False

    if ok and "<title>Domo - Blocked</title>" in res.text:
        ip_address = find_ip(res.text)

        raise BlockedByVPN(auth.domo_instance, ip_address)

    if ok:
        try:
            if "application/json" in res.headers.get("Content-Type", {}):
                return cls(
                    status=res.status_code,
                    response=res.json(),
                    is_success=True,
                    auth=auth,
                    traceback_details=traceback_details,
                    parent_class=parent_class,
                    url=res.url,
                    body=res.request.body if hasattr(res.request, "body") else None,
                )

        except Exception:
            return cls(
                status=res.status_code,
                response=res.text,
                is_success=True,
                auth=auth,
                traceback_details=traceback_details,
                parent_class=parent_class,
                url=res.url,
                body=res.request.body if hasattr(res.request, "body") else None,
            )

        # default text responses
        return cls(
            status=res.status_code,
            response=res.text,
            is_success=True,
            auth=auth,
            traceback_details=traceback_details,
            parent_class=parent_class,
            url=res.url,
            body=res.request.body if hasattr(res.request, "body") else None,
        )

    # errors
    return cls(
        status=res.status_code,
        response=res.reason_phrase,
        is_success=False,
        auth=auth,
        traceback_details=traceback_details,
        parent_class=parent_class,
        url=res.url,
        body=res.request.body if hasattr(res.request, "body") else None,
    )


STREAM_FILE_PATH = "__large-file.json"


async def _write_stream(
    res: httpx.Response, file_name: str = STREAM_FILE_PATH, stream_chunks=10
):
    print(type(res), type(res.content), stream_chunks)

    index = 0
    with open(file_name, "wb") as fd:
        async for chunk in res.content.iter_chunked(1024):
            index += 1
            print(f"writing chunk - {index}")
            fd.write(chunk)

            print(res.content.at_eof())

    print("done writing stream")

    return None


async def _read_stream(file_name: str):
    with open(file_name, "rb") as f:
        return f.read()


@patch_to(ResponseGetData, cls_method=True)
async def _from_looper(
    cls: ResponseGetData, res: ResponseGetData, array: list  # requests response object
) -> ResponseGetData:
    """async method returns ResponseGetData"""

    if not res.is_success:
        return res

    res.response = array
    return res