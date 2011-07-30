import requests
import json
import functools


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
        #return json.load(response)
        return json.loads(response.content)

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
        return functools.partial(self._request, method.replace('_', '.'))
