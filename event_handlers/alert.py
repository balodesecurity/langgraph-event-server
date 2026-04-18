def handle_alert(payload: dict) -> str:
    """Process an alert event — this is where triage logic would go."""
    alert_id = payload.get("alert_id", "unknown")
    service = payload.get("service", "unknown")
    return f"Processed alert {alert_id} for service {service}"
