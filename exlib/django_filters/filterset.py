from django_filters.rest_framework import FilterSet
from django import forms
from django_filters.constants import ALL_FIELDS, EMPTY_VALUES, STRICTNESS
import django_filters
import six
from collections import OrderedDict
from django_filters.filterset import get_full_clean_override
from django_filters.fields import Lookup
from django.db.models import Q


class SfieldFilterSet(FilterSet):
    @property
    def form(self):
        if not hasattr(self, '_form'):
            fields = OrderedDict([
                (filter_.name, filter_.field)
                for name, filter_ in six.iteritems(self.filters)])

            Form = type(str('%sForm' % self.__class__.__name__),
                        (self._meta.form,), fields)
            if self._meta.together:
                Form.full_clean = get_full_clean_override(self._meta.together)
            if self.is_bound:
                self._form = Form(self.data, prefix=self.form_prefix)
            else:
                self._form = Form(prefix=self.form_prefix)
        return self._form


class NatualFilterSet(SfieldFilterSet):
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            if not self.is_bound:
                self._qs = self.queryset.all()
                return self._qs

            if not self.form.is_valid():
                if self.strict == STRICTNESS.RAISE_VALIDATION_ERROR:
                    raise forms.ValidationError(self.form.errors)
                elif self.strict == STRICTNESS.RETURN_NO_RESULTS:
                    self._qs = self.queryset.none()
                    return self._qs
                    # else STRICTNESS.IGNORE...  ignoring

            # start with all the results and filter from there
            qs = self.queryset.all()
            for name, filter_ in six.iteritems(self.filters):
                value = self.form.cleaned_data.get(name) or self.form.cleaned_data.get(filter_.name)

                if value not in [None, '']:  # valid & clean data
                    qs = filter_.filter(qs, value)

            self._qs = qs

        return self._qs


class CommaSeparatedCharFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        conditions = [
            {'%s__startswith' % self.field_name: '%s,' % value},
            {'%s__endswith' % self.field_name: ',%s' % value},
            {'%s__contains' % self.field_name: ',%s,' % value},
        ]
        q = None
        for con in conditions:
            q = Q(**con) if q is None else (q | Q(**con))
        qs = self.get_method(qs)(q)
        return qs


class CommonModelMultipleChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    """
        当查询字段to_field_name和关联字段rel_field_name不同时使用
        但：to_field_name 会占用掉id的查询。
    """
    def __init__(self, *args, **kwargs):
        self.rel_field_name = kwargs.pop('rel_field_name')
        super(CommonModelMultipleChoiceFilter, self).__init__(*args, **kwargs)

    def get_filter_predicate(self, v):
        try:
            if self.rel_field_name:
                return {self.field_name: getattr(v, self.field.rel_field_name)}
            else:
                return {self.field_name: getattr(v, self.field.to_field_name)}
        except (AttributeError, TypeError):
            return {self.field_name: v}


class UnionFilterSet(SfieldFilterSet):
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            if not self.is_bound:
                self._qs = self.queryset.all()
                return self._qs

            if not self.form.is_valid():
                if self.strict == STRICTNESS.RAISE_VALIDATION_ERROR:
                    raise forms.ValidationError(self.form.errors)
                elif self.strict == STRICTNESS.RETURN_NO_RESULTS:
                    self._qs = self.queryset.none()
                    return self._qs
                    # else STRICTNESS.IGNORE...  ignoring

            # start with all the results and filter from there
            qs = self.queryset.all()
            condition = None
            for name, filter_ in six.iteritems(self.filters):
                value = self.form.cleaned_data.get(name) or self.form.cleaned_data.get(filter_.name)

                if value not in [None, '']:  # valid & clean data
                    d = {name: value}
                    if condition is None:
                        condition = Q(**d)
                    else:
                        condition = condition | Q(**d)
            self._qs = qs.filter(condition) if condition is not None else qs

        return self._qs
