def validateAlias(name : str) -> bool:
    return len(str) < 20 and len(name) == len(name.encode())