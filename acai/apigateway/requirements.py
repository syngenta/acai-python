import inspect


def requirements(**kwargs):
    def decorator_func(func):

        def run_before(request, response):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](request, response, kwargs)

        def run_after(request, response):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](request, response, kwargs)

        def run_method(request, response):
            run_before(request, response)
            if not response.has_errors and kwargs.get('data_class') and inspect.isclass(kwargs['data_class']):
                data_class = kwargs['data_class'](request=request)
                func(data_class, response)
            elif not response.has_errors:
                func(request, response)
            if not response.has_errors:
                run_after(request, response)
            return response

        run_method.requirements = kwargs
        return run_method

    return decorator_func
