import requests
import json


class GlitchAPI(object):
    DOMAIN = 'api.glitch.com'
    BASE_PATH = '/simple'

    def __init__(self, access_token=None):
        """
        Pass an `access_token` if you need it.
        Not all methods require one.
        """
        super(GlitchAPI, self).__init__()
        self.access_token = access_token

    def _request(self, method, **kwargs):
        """
        Helper function to invoke `method` with the `kwargs` such as
        `player_tsid` or `per_page`.
        """
        if self.access_token:
            kwargs['oauth_token'] = self.access_token

        response = requests.get(self._uri(method),
                                params=kwargs)

        return self._postprocess(response)

    def _postprocess(self, response):
        """
        Makes modifications to the response object before returning it.

        If you don't want to throw exceptions, or parse json, override this
        and just return `response`
        """
        response.raise_for_status()

        # For some reason, this doesn't work.
        #response.content = json.load(response)
        response.content = json.loads(response.content)

        return response

    def _uri(self, path):
        """
        Builds the URI to actually hit.  If you're on a dev or alpha
        channel, just subclass this to something like GlitchAlphaAPI
        """
        return 'http://' + self.DOMAIN + self.BASE_PATH +'/' + path

    def __getattr__(self, method):
        """
        The magic happens here.  Just call the API method with _'s instead of
        "."s, and it returns a requests.model.Response instance.
        """
        return _ProxyCall(self, method.replace('_', '.'))


class _ProxyCall(object):
    """
    Wrapper for returning dynamically defined API methods.
    There is no whitelist of methods.

    See http://api.glitch.com/ for documentation
    """
    def __init__(self, api, method):
        super(_ProxyCall, self).__init__()
        self.api = api
        self.method = method

    def __call__(self, **kwargs):
        return self.api._request(self.method, **kwargs)
