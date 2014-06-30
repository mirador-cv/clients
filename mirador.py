import base64
import requests


class MiradorResult(object):
    """
    A result from the Mirador API.
    Contains fields indicating classification result:

    safe - boolean value indicating whether image
    was categoried as "sfw" (true) or "nsfw"

    value - a float 0.0-1.0 representing the confidence of the classification
    """

    FMT_STR = "<MiradorResult: {name}; safe: {safe}; value: {value}/>"

    def __init__(self, name, raw={}):

        if 'result' not in raw:
            return None

        res = raw.get('result', {})

        self.name = name
        self.safe = res.get('safe', None)
        self.value = res.get('value', None)

    @staticmethod
    def parse_results(reqs, results):
        """ parse JSON output of API into MiradorResult objects """

        if not results:
            return None

        return [
            MiradorResult(n, r)
            for n, r in zip(reqs, results)
        ]

    def __repr__(self):
        return self.FMT_STR.format(**self.__dict__)


class MiradorClientException(Exception):
    """ Basic exception subclass for Mirador API errors """

    def __init__(self, status, msg):
        self.status_code = status

        super(
            MiradorClientException, self
        ).__init__("[{}]: {}".format(status, msg))


class MiradorClient(object):
    """

    """

    API_BASE = "http://api.mirador.im"
    CLASSIFY_ENDPOINT = "/v1/classify"
    TIMEOUT = 10
    HEADERS = {
        'User-Agent': 'MiradorClient/1.0 Python'
    }

    def __init__(self, api_key):
        self._api_key = api_key

    def _request(self, data={}):

        if not data or ('image' not in data and 'url' not in data):
            raise MiradorClientException(400, "url(s) or image(s) required")

        m = 'get' if 'url' in data else 'post'

        url = "{0}{1}".format(
            self.API_BASE, self.CLASSIFY_ENDPOINT, self._api_key)

        data['api_key'] = self._api_key

        req = {'headers': self.HEADERS}
        req['data' if m == 'post' else 'params'] = data

        r = getattr(requests, m)(url, **req)

        if r.status_code != 200:
            raise MiradorClientException(r.status_code, r.text)

        return r.json()

    def _prepare_image(self, im_f):

        image_data = None
        name = None

        if isinstance(im_f, basestring):
            name = im_f
            with open(im_f, 'r') as imf:
                image_data = imf.read()
        else:
            name = im_f.name
            image_data = im_f.read()

        if not image_data:
            raise MiradorClientException(
                400, "no image data for file: {}".format(name))

        return base64.b64encode(image_data)

    def classify_urls(self, *urls):
        res = self._request(data={'url': urls})
        return MiradorResult.parse_results(
            urls, res.get('results', None))

    def classify_files(self, *files):
        res = self._request(data={'image': map(self._prepare_image, files)})

        return MiradorResult.parse_results(
            files, res.get('results', None))


if __name__ == "__main__":
    import sys

    client = MiradorClient('your_key_here')
    files = sys.argv[1:]

    for res in client.classify_files(*files):
        print res
