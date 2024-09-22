from http import HTTPStatus, HTTPMethod
from typing import Optional
from urllib.parse import urljoin

import requests
from requests import Response

from api.exceptions.api_exception import ApiException
from logs.logger import Logger


class ApiClient:
    def __init__(self, base_url: str, base_headers: dict):
        self.__base_url = base_url
        self.__base_headers = base_headers

    def get(self, path: str = None, query_params: list[tuple] = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.get(url, headers=self.__base_headers, params=query_params)
        return self.__resolve_response(HTTPMethod.GET, url, response)

    def put(self, body: str, path: str = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.put(url, headers=self.__base_headers, data=body.encode(encoding='utf-8'))
        return self.__resolve_response(HTTPMethod.PUT, url, response)

    def post(self, body: str, path: str = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.post(path, headers=self.__base_headers, data=body.encode(encoding='utf-8'))
        return self.__resolve_response(HTTPMethod.POST, url, response)

    def delete(self, path: str) -> Optional[str]:
        url = urljoin(self.__base_url, path)
        response = requests.delete(path, headers=self.__base_headers)
        return self.__resolve_response(HTTPMethod.DELETE, url, response)

    @staticmethod
    def __resolve_response(http_method: str, url: str, response: Response) -> Optional[str]:
        if response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.CREATED:
            Logger.info(f'API success: url={url}')
            return response.text  # format: xml
        else:
            raise ApiException(http_method, url, response.status_code, response.reason, response.text)

    @property  # for Testing
    def base_url(self) -> str:
        return self.__base_url

    @property  # for Testing
    def base_headers(self) -> dict:
        return self.__base_headers
