#-*- coding: utf-8 -*-
from django import template

from kbo.models import Standing

register = template.Library()

@register.filter()
def format_pct(value):
    return '{pct:.3f}'.format(pct = value / 1000.0)

@register.filter()
def format_gb(value):
    return '{pct:.1f}'.format(pct = value / 10.0)

@register.filter()
def format_streak(value):
    if value != 0:
        ret = '{number}{win_loss}'.format(
            number = abs(value),
            win_loss = '승' if value > 0 else '패',
        )
    else:
        ret = '-'
    return ret

@register.filter()
def format_l10(value):
    w = 0
    l = 0
    d = 0
    for s in value:
        if s == Standing.WIN:
            w += 1
        elif s == Standing.LOSS:
            l += 1
        else:
            d += 1

    return '{w}승-{d}무-{l}패'.format(
        w = w,
        d = d,
        l = l,
    )

