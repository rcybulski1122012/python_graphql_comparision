import re
from typing import NewType

import strawberry
from graphql import GraphQLError
from strawberry_django.fields.types import field_type_map

from python_graphql_comparison.utils.fields import HexColorField


def parse_color_code(v: str) -> str:
    if not re.match(HexColorField.hex_regex, v):
        message = f"Invalid color code: {v}"
        raise GraphQLError(message)

    return v


ColorCode = strawberry.scalar(
    NewType("ColorCode", str),
    serialize=lambda v: v,
    parse_value=parse_color_code,
    description="Color code in hex format. For example: #FF12FF or #FFF.",
)

field_type_map.update(
    {
        HexColorField: ColorCode,
    }
)
