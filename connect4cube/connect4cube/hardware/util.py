def is_a_raspberry():
    try:
        import RPi.GPIO  # noqa: F401
        return True
    except (ImportError, RuntimeError):
        return False
