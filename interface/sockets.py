import json
from socketio.mixins import RoomsMixin
from socketio.sdjango import namespace
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace


@namespace('/streaming')
class SocketI2CNamespace(BaseNamespace, BroadcastMixin, RoomsMixin):
    def on_push_data_api(self, json_):
        self.broadcast_event_not_me('broadcast', json.dumps(json_))
