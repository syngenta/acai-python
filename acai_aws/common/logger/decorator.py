from acai_aws.common import logger


def log(**settings):
    def decorator_func(func):
        captured = {'arguments': {}, 'result': None}

        def run_func(*args, **kwargs):
            captured['arguments']['args'] = list(args)
            captured['arguments']['kwargs'] = kwargs
            captured['result'] = func(*args, **kwargs)
            if settings.get('condition') and callable(settings['condition']):
                if settings['condition'](*args, **kwargs):
                    logger.log(level=settings.get('level', 'INFO'), log=captured)
            else:
                logger.log(level=settings.get('level', 'INFO'), log=captured)
            return captured['result']

        return run_func

    return decorator_func
