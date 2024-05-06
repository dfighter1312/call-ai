from urllib.parse import urlparse, parse_qs

from utils.types.api_request import APIRequest


def parse_path(path: str) -> APIRequest:
    """
    Parse a URL and return a dictionary of its components.
    """
    # Parse the URL to extract query parameters
    url = urlparse(path)
    query_params = parse_qs(url.query)

    # Extract user_id and scenario_id from the query parameters
    parameters = {key: val[0] for key, val in query_params.items()}

    request_object = APIRequest(path=url.path, **parameters)
    return request_object
