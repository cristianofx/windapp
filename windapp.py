import http.client, urllib
import requests
import time
from plyer import notification

# Function to get data from the API
def get_data():
    url = "https://api.weatherapi.com/v1/current.json?key=<YOUR_KEY>&q=Lisbon"
    response = requests.get(url)
    return response.json()

# Function to get wind direction from the DATA
def get_wind_direction(data):
    return data['current']['wind_dir']

# Function to get last updated from the DATA
def get_last_updated(data):
    return data['current']['last_updated']

# Function to send notification
def send_notification(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "<Pushover Application Token>",
        "user": "<Pushover User Token>",
        "message": f'{message}',
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Function to create the message based on wind direction
def create_message(direction, last_updated):
    if 'S' in direction:
        return f"Wind direction changed, now FROM {direction}, last updated {last_updated}. LUCKY US!"
    elif 'N' in direction:
        return f"Wind direction changed, now FROM {direction}, last updated {last_updated}. OH NO!!!"
    else:
        return f"Wind direction changed, now FROM {direction}, last updated {last_updated}."

def main():
    last_direction = None
    while True:
        try:
            print("Getting data")
            data = get_data();
            current_direction = get_wind_direction(data)
            current_last_updated = get_last_updated(data)
            if current_direction != last_direction:
                message = create_message(current_direction, current_last_updated)
                send_notification(message)
                last_direction = current_direction
            print("sleeping 60 seconds")
            time.sleep(60)  # Check every 1 minute
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(300)  # Wait before retrying

if __name__ == "__main__":
    main()
