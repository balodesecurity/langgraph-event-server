def handle_deploy(payload: dict) -> str:
    """Process a deployment event — could trigger smoke tests, notifications, etc."""
    version = payload.get("version", "unknown")
    return f"Acknowledged deploy of version {version}"
