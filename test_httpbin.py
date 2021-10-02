import pytest
import logging
import requests


log = logging.getLogger('urllib3')  # works
log.setLevel(logging.DEBUG)  # needed
fh = logging.FileHandler("requests.log")
log.addHandler(fh)


def test_header_ok():
    url_headers = "http://httpbin.org/headers"
    r = requests.get(url_headers, headers={'One': 'true'})
    assert "OK" == r.reason
    assert r.json()['headers']['One'] == 'true'


def test_header_incorrect_request():
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(
            "http://httpbin.org/headers",
            headers={'Content-Length': '200'}
        )


def test_status_multiples_code():
    codes = [200, 300, 400, 500]
    url_all_code = "http://httpbin.org/status/" + ",".join(map(str, codes))
    r = requests.get(url_all_code)
    assert r.status_code in codes


@pytest.mark.parametrize(
    "request_type",
    [
        requests.get,
        requests.post,
        requests.put,
        requests.delete,
        requests.patch
    ]
)
@pytest.mark.parametrize("code", [200, 300, 400, 500])
def test_status_code(code, request_type):
    url_all_code = "http://httpbin.org/status/" + str(code)
    r = request_type(url_all_code)
    assert r.status_code == code
