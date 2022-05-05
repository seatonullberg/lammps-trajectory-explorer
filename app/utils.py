def has_method(obj, name):
    """Returns True if `obj` has a method by the given `name` else False.

    Args:
        obj: Any object.
        name: Method name.
    """
    attr = getattr(obj, name, None)
    return callable(attr)
