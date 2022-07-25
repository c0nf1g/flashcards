import typing as t
from _typeshed.wsgi import WSGIEnvironment

from werkzeug.exceptions import Unauthorized


class ApiUnauthorized(Unauthorized):
    def __init__(
            self,
            description="Unauthorized",
            error=None,
            error_description=None,
    ):
        self.description = description
        self.www_auth_value = self.__get_www_auth_value(
            error, error_description
        )
        Unauthorized.__init__(
            self, description=description, response=None, www_authenticate=None
        )

    def get_headers(
        self,
        environ: t.Optional["WSGIEnvironment"] = None,
        scope: t.Optional[dict] = None
    ) -> t.List[t.Tuple[str, str]]:
        return [("Content-Type", "text/html"), ("WWW-Authenticate", self.www_auth_value)]

    def __get_www_auth_value(self, error, error_description):
        www_auth_value = 'Bearer realm="Flashcards application"'
        if error:
            www_auth_value += f', error="{error}"'
        if error_description:
            www_auth_value += f', error_description="{error_description}"'
        return error_description
