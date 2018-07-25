# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import RelatedField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict


class RepresentField(RelatedField):
    """
        when it can be empty you need config  allow_null=True, required=False
    """
    default_error_messages = {
        'does_not_exist': _('Object with {slug_name}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, repr_fields=None, **kwargs):
        assert repr_fields is not None, 'The `repr_field` argument is required.'
        self.repr_fields = repr_fields
        super(RepresentField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', repr_name=self.repr_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        if len(self.repr_fields) == 1:
            return getattr(obj, self.repr_fields[0])
        res = {attr: getattr(obj, attr) for attr in self.repr_fields}
        return res

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        if cutoff is not None:
            queryset = queryset[:cutoff]
        return OrderedDict([
            (
                getattr(item, 'pk'),
                self.display_value(item)
            )
            for item in queryset
        ])