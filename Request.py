from dataclasses import dataclass

@dataclass
class Request:
    request: str
    response: str
    response_code: int
    err_msg: str



