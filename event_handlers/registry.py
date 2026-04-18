from event_handlers.alert import handle_alert
from event_handlers.deploy import handle_deploy
from event_handlers.stock import handle_stock

# Registry of event_type -> handler function.
# To support a new event type, write a handler function and add it here.
HANDLERS = {
    "alert_fired": handle_alert,
    "deploy_completed": handle_deploy,
    "stock_query": handle_stock,
}
