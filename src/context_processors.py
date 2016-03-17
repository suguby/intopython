# -*- coding: utf-8 -*-


def common_variables_to_context(request):
    return dict(
        user=request.user,
        bltn=__builtins__,
    )

