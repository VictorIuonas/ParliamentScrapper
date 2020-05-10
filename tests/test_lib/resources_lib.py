import os

import scrapy


def fake_response_from_file(file_name: str, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = scrapy.http.Request(url=url)
    if not file_name[0] == '/':
        responses_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    file_content = open(file_path, 'r').read()

    response = scrapy.http.HtmlResponse(
        encoding='utf-8',
        url=url,
        request=request,
        body=file_content
    )

    return response
