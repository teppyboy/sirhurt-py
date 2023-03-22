class ExploitError(Exception):
    pass


class InjectError(ExploitError):
    pass


class NotInjectedError(InjectError):
    pass


class AlreadyInjectedError(InjectError):
    pass
