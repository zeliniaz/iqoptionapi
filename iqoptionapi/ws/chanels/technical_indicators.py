import datetime
import time
from iqoptionapi.ws.chanels.base import Base


class Technical_indicators_subscribe(Base):
    name = "subscribeMessage"

    def __call__(self, active):
        data = {
            "name": "trading-signals.get-technical-indicators",
            "version": "1.0",
            "body": {
                "id": active
            }
        }
        request_id = int(str(time.time()).split('.')[1])
        self.send_websocket_request(self.name, data, request_id)
        return request_id


class Technical_indicators_unsubscribe(Base):
    name = "unsubscribeMessage"

    def __call__(self, active):
        data = {
            "name": "trading-signals.get-technical-indicators",
            "version": "1.0",
            "body": {
                "id": active
            }
        }

        self.send_websocket_request(self.name, data)