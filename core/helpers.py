from typing import Callable
from secrets import token_urlsafe
from jdatetime import datetime as jdt

from django.urls import reverse
from django.db import transaction
from django.dispatch import receiver
from django.utils.timezone import localtime
from django.utils.html import format_html, urlencode


def uuid_generator():
    return token_urlsafe(8).replace("-", "x").replace("_", "j")


def gregorian_to_jalali(time):
    return jdt.fromgregorian(date=localtime(time)).strftime("%Y-%m-%d %H:%M:%S")


def model_change_url_to_html(app, model, args, placeholder):
    url = reverse(f"admin:{app}_{model}_change", args=args)
    return format_html('<a href="{}">{}</a>', url, placeholder)


def model_changelist_url_to_html(app, model, query_key, query_val, placeholder):
    url = (
        reverse(f"admin:{app}_{model}_changelist")
        + "?"
        + urlencode({query_key: str(query_val)})
    )
    return format_html('<a href="{}">{}</a>', url, placeholder)


def image_url_to_html(image, style, width=None, height=None, open_in_new_tab=False):
    if image.name != "":
        url = image.url
        open_in_new_tab = 'target="_blank"' if open_in_new_tab else ""
        width = f'width="{width}"' if width else ""
        height = f'height="{height}"' if height else ""
        return format_html(
            f'<a href="{url}" {open_in_new_tab}>'
            f'<img src="{url}" {width} {height} style="object-fit:{style};"/>'
             '</a>'
        )
    return ""


def receiver_with_dirty_transaction(*receiver_args, **receiver_kwargs):
    def _wrapper(func: Callable):
        @receiver(*receiver_args, **receiver_kwargs)
        def _decorator(sender, instance, **kwargs):
            def _inner():
                instance._dirty = True
                func(sender, instance, **kwargs)
                instance._dirty = False
            if not getattr(instance, '_dirty', False):
                transaction.on_commit(_inner)
        return _decorator
    return _wrapper
