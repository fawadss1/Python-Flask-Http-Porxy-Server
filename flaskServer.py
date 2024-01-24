from urllib.parse import urlparse
from flask import Flask, request, make_response
import requests
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@app.route('/fetch')
def fetch():
    proxy = request.args.get('proxy')
    target_url = request.args.get('url')

    if not target_url or not proxy:
        return "URL or Proxy not provided", 400

    if not is_valid_url(target_url):
        return "Invalid URL", 400

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    if proxy != 'None':
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
    else:
        proxies = None

    try:
        response = requests.get(url=target_url, headers=headers, proxies=proxies, timeout=10)
        logging.info(f"Request Response Status: {response.status_code}")
        flaskResponse = make_response(response.content)
        flaskResponse.headers['flaskResponseCode'] = str(response.status_code)
        return flaskResponse
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return str(e), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
