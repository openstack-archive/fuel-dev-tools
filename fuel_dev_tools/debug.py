import six


class DebugMixin(object):
    def __init__(self, app, parsed_args):
        super(DebugMixin, self).__init__(app, parsed_args)

        self._debug = getattr(parsed_args, 'debug', False)

    def print_debug(self, msg):
        if self._debug:
            six.print_(msg)
