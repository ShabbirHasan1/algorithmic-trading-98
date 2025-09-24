from NorenRestApiPy.NorenApi import *
import logging
import pyotp

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')
        global api
        api = self

    # Expose the WebSocket instance
    @property
    def ws(self):
        return self.websocket

logging.basicConfig(level=logging.INFO)  # Enable debug to see request and responses

api = ShoonyaApiPy()  # Start of our program

def login():
    # Generation of TOTP and Initializing it to "otp"
    token = 'J42QW26PID6FZV6E4WCO3K3326T6BA6W'  # Token to generate totp
    otp = pyotp.TOTP(token).now()  # TOTP is generated & loaded into otp variable

    # Login credentials
    user = '**********'  # UID
    pwd = '**********'  # Password         
    vc = "**********"  # Vendor code from prism
    app_key = "f91385ce18e8afeadae040**********"  # API key from prism
    imei = "abc1234"  # IMEI from Shoonya Prism

    # Calling Login Method on api Instance (created at the start of the program)
    ret = api.login(userid=user, password=pwd, twoFA=otp, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret

def logout():
    api.logout()

login()

def start_websocket(order_update_callback, subscribe_callback, socket_open_callback):
    api.start_websocket(order_update_callback=order_update_callback,
                        subscribe_callback=subscribe_callback,
                        socket_open_callback=socket_open_callback)

def subscribe_instruments(instruments):
    """Subscribe to a list of instruments."""
    if isinstance(instruments, list):
        api.subscribe(instruments)
    else:
        api.subscribe([instruments])  # Wrap single instrument in a list

# Event handlers
def event_handler_feed_update(tick_data):
    print(f"Feed update: {tick_data}")

def event_handler_order_update(tick_data):
    print(f"Order update: {tick_data}")

feed_opened = False

def open_callback():
    global feed_opened
    feed_opened = True