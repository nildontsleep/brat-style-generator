import webview
from screeninfo import get_monitors
import os
import sys
import base64

def resource_path(relative_path):
    """
    Get absolute path for resources, works both in development and when bundled by PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

# Get primary monitor resolution
monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

# Choose maximum height to fit 9:16 ratio inside the screen
max_height = int(screen_height * 0.9)
max_width = int(max_height * 9 / 16)

# Ensure it doesn't exceed screen width
if max_width > screen_width * 0.9:
    max_width = int(screen_width * 0.9)
    max_height = int(max_width * 16 / 9)

# Path to HTML file
html_file = resource_path("index.html")

# Python API exposed to JS
class API:
    def save_image(self, data_url):
        """
        Save the base64 image sent from JavaScript.
        """
        try:
            # Remove the header 'data:image/png;base64,'
            header, encoded = data_url.split(',', 1)
            data = base64.b64decode(encoded)

            filename = "brat-style.png"
            with open(filename, "wb") as f:
                f.write(data)
            return f"Saved as {filename}"
        except Exception as e:
            return f"Error saving image: {str(e)}"

# Create API instance
api = API()

# Create the window
webview.create_window(
    "Brat Style Generator",
    html_file,
    width=max_width,
    height=max_height,
    resizable=True,
    min_size=(400, 500),
    js_api=api  # <-- expose the API to JS
)

webview.start()
