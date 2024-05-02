from http import HTTPStatus, HTTPMethod
from typing import Optional
from urllib.parse import urljoin

import requests
from requests import Response

from docs_and_blog_entries_manager.exceptions.api_exception import ApiException
from docs_and_blog_entries_manager.logs.logger import Logger


class ApiClient:
    def __init__(self, base_url: str, base_headers: dict):
        self.__base_url = base_url
        self.__base_headers = base_headers

    def get(self, path: str = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.get(url, headers=self.__base_headers)
        return self.__resolve_response(HTTPMethod.GET.value(), url, response)

    def put(self, body: bytes, path: str = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.put(url, headers=self.__base_headers, data=body)
        return self.__resolve_response(HTTPMethod.PUT.value(), url, response)

    def post(self, body: bytes, path: str = None) -> Optional[str]:
        url = self.__base_url if path is None else urljoin(self.__base_url, path)
        response = requests.post(path, headers=self.__base_headers, data=body)
        return self.__resolve_response(HTTPMethod.POST.value(), url, response)

    def delete(self, path: str) -> Optional[str]:
        url = urljoin(self.__base_url, path)
        response = requests.delete(path, headers=self.__base_headers)
        return self.__resolve_response(HTTPMethod.DELETE.value(), url, response)

    @staticmethod
    def __resolve_response(http_method: str, url: str, response: Response) -> Optional[str]:
        print(response.status_code, response.reason, http_method, url)
        if response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.CREATED:
            Logger.info(f'API success: url={url}')
            return response.text  # format: xml
        else:
            raise ApiException(http_method, url, response.text)
