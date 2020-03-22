import datetime
import time
from iqoptionapi.ws.chanels.base import Base
import logging
import iqoptionapi.global_value as global_value
from iqoptionapi.expiration import get_expiration_time


class Buyv3(Base):

    name = "sendMessage"

    def __call__(self, price, active, direction, duration, request_id):

        # thank Darth-Carrotpie's code
        # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
        exp, idx = get_expiration_time(
            int(self.api.timesync.server_timestamp), duration)
        if idx < 5:
            option = 3  # "turbo"
        else:
            option = 1  # non-turbo / binary
        data = {
            "body": {"price": price,
                     "active_id": active,
                     "expired": int(exp),
                     "direction": direction.lower(),
                     "option_type_id": option,
                     "user_balance_id": int(global_value.balance_id)
                     },
            "name": "binary-options.open-option",
            "version": "1.0"
        }
        self.send_websocket_request(self.name, data, str(request_id))


class Buyv3_by_raw_expired(Base):

    name = "sendMessage"

    def __call__(self, price, active, direction, option, expired, request_id):

        # thank Darth-Carrotpie's code
        # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6

        if option == "turbo":
            option_id = 3  # "turbo"
        elif option == "binary":
            option_id = 1  # "binary"
        data = {
            "body": {"price": price,
                     "active_id": active,
                     "expired": int(expired),
                     "direction": direction.lower(),
                     "option_type_id": option_id,
                     "user_balance_id": int(global_value.balance_id)
                     },
            "name": "binary-options.open-option",
            "version": "1.0",
            "body": {
                "user_balance_id": int(self.api.profile.balance_id),
                "active_id": active,
                "option_type_id": option,
                "direction": direction.lower(),
                "expired": int(exp),
                "refund_value": 0,
                "price": price,
                "value": 0,  # Preset to 0, don't worry won't affect the actual buy contract
                # IQOption accept any value lower than the actual percent, don't worry it won't affect actual earning
                "profit_percent": 0
            }
        }
        self.send_websocket_request(self.name, data, str(request_id))
