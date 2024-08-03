import time
from .notification_service import send_notification

def simulate_data_updates():
    """Simulate periodic data updates and send notifications."""
    while True:
        # Simulate data updates (e.g., flight status changes)
        flight_update = "Flight AA123 is now boarding at gate A2."
        send_notification(flight_update)
        
        # Wait for the next update cycle
        time.sleep(60)  # Update every minute

if __name__ == "__main__":
    simulate_data_updates()
