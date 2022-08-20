from jdatetime import datetime as jdt
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.utils.timezone import localtime


def gregorian_to_jalali(time):
    return jdt.fromgregorian(date=localtime(time)).strftime("%Y-%m-%d %H:%M:%S")


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
