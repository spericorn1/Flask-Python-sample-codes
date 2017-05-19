# -*- coding: utf-8 -*-
"""
Signal handlers
"""
from datetime import datetime

from backend.backend.models import Notification


def event_hints(sender, **kw):
    """
    Create hints for an Event when it's saved

    - list + string hints are NOT case sensitive
     - all values are run through `lower()` and `strip()`
    """
    if not kw.get('created', False):
        return

    event = kw.get('instance')
    hints = []  # hints have been neutered

    def match(event_value, hint):
        """
        Function to compare a hint against an event_value
        """
        value_class = event_value.__class__.mro()
        if list in value_class:
            event_value = [value.lower().strip() for value in event_value]
            matches = [
                getattr(event_value, hint.field_comparison)(
                    value.lower().strip())
                for value in hint.value.split(',')]
            match = reduce(lambda x, y: x and y, matches)
        elif int in value_class:
            comparison = cmp(event_value, int(hint.value))
            if comparison == 0 \
                    and hint.field_comparison == '__eq__':
                match = True
            elif comparison == -1 \
                    and hint.field_comparison == '__lt__':
                match = True
            elif comparison == 1 \
                    and hint.field_comparison == '__gt__':
                match = True
            else:
                match = False

        else:
            if datetime in value_class:
                # current_app not available here, outside of application
                # context; this string is copied from
                # backend/backend/settings.py
                value = datetime.strptime(hint.value, '%Y-%m-%dT%H:%M:%S.%fZ')
            elif basestring in value_class:
                event_value = event_value.lower().strip()
                value = hint.value.lower().strip()
            else:
                value = None

            match = getattr(event_value, hint.field_comparison)(value)

        return match

    for hint in hints:
        event_value = getattr(event, hint.field_name)
        if not event_value:
            continue

        try:
            hint_applies = match(
                event_value=event_value,
                hint=hint,
            )
        except KeyError:
            pass
        else:
            if hint_applies:
                Notification(
                    user_for=event.owner,
                    target=event,
                    text=hint.text,
                ).save()
