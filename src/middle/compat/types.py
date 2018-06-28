import sys
import typing
from datetime import date
from datetime import datetime
from decimal import Decimal
from enum import EnumMeta

if sys.version_info >= (3, 7):
    from typing import _GenericAlias as GenericType
else:
    from typing import GenericMeta as GenericType


TYPE_REGISTRY = {}


def get_type(type_):
    if type_ is None:
        return type(None)
    if type_ in (
        str,
        int,
        float,
        bool,
        list,
        dict,
        set,
        date,
        datetime,
        bytes,
        Decimal,
    ):
        return type_
    tt = type(type_)
    if hasattr(tt, "__module__") and tt.__module__ == "typing":
        if tt == GenericType:
            if hasattr(type_, "__base__"):  # py3.6
                return type_.__base__
            elif hasattr(type_, "__origin__"):
                if hasattr(type_, "_name") and isinstance(type_._name, str):
                    return getattr(typing, type_._name)  # py3.7
                return type_.__origin__
        elif hasattr(typing, "_Union") and tt == typing._Union:  # py36
            return typing.Union
        elif hasattr(typing, "TupleMeta") and tt == typing.TupleMeta:  # py36
            return typing.Tuple
    elif tt == EnumMeta:
        return tt
    elif tt in TYPE_REGISTRY:
        return TYPE_REGISTRY[tt]