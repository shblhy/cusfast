import datetime
from django.core.serializers.json import DjangoJSONEncoder


class DjangoTJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H-%M-%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return DjangoJSONEncoder.default(self, o)