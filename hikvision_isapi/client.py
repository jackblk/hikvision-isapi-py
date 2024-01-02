import logging
import os
from typing import Literal

import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError


class HikvisionHeadersTemplate:
    DEFAULT = None
    REQ_XML = {
        "Content-Type": "application/xml",
    }


class HikvisionClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        verify_ssl: bool = True,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        if "" in [base_url, username, password]:
            raise ValueError(
                "Vars not configured correctly. "
                f"Base URL: {base_url}, username: {username}, password: {password}."
            )
        self.username = username
        self.password = password
        self.base_url = base_url.strip("/")
        self.headers_template = {""}
        self.verify_ssl = verify_ssl
        if os.environ.get("VERIFY_SSL", "True").lower() != "true":
            self.verify_ssl = False

    def _generate_auth(self) -> HTTPDigestAuth:
        return HTTPDigestAuth(username=self.username, password=self.password)

    def request(
        self,
        path: str,
        method="GET",
        headers=HikvisionHeadersTemplate.DEFAULT,
        data=None,
        json=None,
    ):
        url = self.base_url + path
        self.logger.debug(
            f"Requesting to url: {url}, method: {method}, "
            f"data: {data}, json: {json}"
        )
        res = requests.request(
            method=method,
            headers=headers,
            auth=self._generate_auth(),
            url=url,
            data=data,
            json=json,
            verify=self.verify_ssl,
        )
        # self.logger.debug(res.request.headers)
        # try:
        #     res.raise_for_status()
        # except HTTPError as err:
        #     self.logger.error(
        #         f"Requesting to url: {url}, method: {method}, "
        #         f"data: {data}, json: {json}"
        #     )
        #     raise err
        return res

    def get_access_control_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/capabilities",
        )
        return res

    def get_door_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/RemoteControl/door/capabilities",
        )
        return res

    def remote_control_door(
        self,
        door_id: str,
        command: Literal["open", "close", "alwaysOpen", "alwaysClose"],
    ):
        door_data_template = (
            f"<RemoteControlDoor><cmd>{command}</cmd></RemoteControlDoor>"
        )
        res = self.request(
            method="PUT",
            path=f"/ISAPI/AccessControl/RemoteControl/door/{door_id}",
            headers=HikvisionHeadersTemplate.REQ_XML,
            data=door_data_template,
        )
        self.logger.debug(
            f"Remote control res: {res.status_code} | {res.headers} | {res.text}"
        )
        return res

    def get_door_security_module_status_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/RemoteControl/door/capabilities",
        )
        return res
