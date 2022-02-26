from .app_exceptions import AppExceptionCase

# referenced blog
"""https://camillovisini.com/article/abstracting-fastapi-services/?fbclid=IwAR355lkTqUo71TvfsPp8rNamBndAZjmuoiO-aRkO-cA_Wy8GCK6m_0GmQ14"""  # noqa E501


class ServiceResult:
    def __init__(self, arg, **kwargs):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = kwargs.get("status_code")
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            raise exception
    with result as result:
        return result
