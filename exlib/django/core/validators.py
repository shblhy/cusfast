from django.core.validators import RegexValidator, _lazy_re_compile

telephone_re = _lazy_re_compile(r'^[0-9]{11}\Z')
validate_telephone = RegexValidator(
    telephone_re,
    '手机号应该为11位数字',
    'invalid'
)
