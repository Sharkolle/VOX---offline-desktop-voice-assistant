def wrap(command_text, result):
    """
    Standardize command handler response.
    - command_text: the original string VOX heard
    - result: dict returned by handler
    """
    if not isinstance(result, dict):
        result = {"text": str(result), "speak": str(result)}
    result["command"] = command_text
    return result
