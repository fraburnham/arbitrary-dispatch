from functools import update_wrapper


def arbitrary_dispatch(dispatch_func):
    def __default__(*args, **kwargs):
        raise Exception("No implementation found for {} on {}".format(
            dispatch_func(*args, **kwargs), dispatch_func
        ))

    registry = {
        "__default__": __default__
    }

    def register(cond, func=None):
        """
        Register a fn for a dispatch condition
        """
        if func is None:
            return lambda f: register(cond, f)

        registry[cond] = func

        return func

    def wrapper(*args, **kwargs):
        fn = registry.get(
            dispatch_func(*args, **kwargs),
            registry.get("__default__")
        )

        return fn(*args, **kwargs)

    wrapper.register = register
    wrapper.registry = registry
    wrapper.dispatch_func = dispatch_func
    update_wrapper(wrapper, dispatch_func)

    return wrapper
