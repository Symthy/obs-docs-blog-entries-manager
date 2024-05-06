class ApiException(Exception):
    def __init__(self, method: str, url: str, request_body: str | None, status_code: int, reason: str,
                 response_body: str | None):
        super().__init__(self.__build_message(method, url, request_body, status_code, reason, response_body))

    def __build_message(self, method: str, url: str, request_body: str | None, status_code: int, reason: str,
                        response_body: str | None):
        req_params = [
            f'api: {method} {url}',
        ]
        if request_body is not None or request_body is not '':
            req_params.append(f'body: {request_body}')
        res_params = [
            f'status: {status_code}',
            f'reason: {reason}'
        ]
        if response_body is not None or response_body is not '':
            res_params.append(f'body: {response_body}')
        return f'API failed.\n  request:({", ".join(req_params)}\n  response:({", ".join(res_params)}))\n'
