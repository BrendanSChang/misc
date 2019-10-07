"""Store context variables.

This module is effectively a singleton for maintaining global state. This
module exposes a single method, `add`, for loading a context into the `ctx`
dict. A context is defined as a set of variables which share the same schema.
See `add` for more details.
"""

import logging
from pprint import pformat
from typing import Sequence

# This dictionary contains the various contexts which have been added via the
# `add` function below. Each context is accessible using its name as the key.
# The value will be a nested dictionary with the first field in the schema as
# the key and the remaining fields stored in a nested dict. See `add` for more
# details.
ctx = {}


def add(name: str, fields: Sequence[str],
        values: Sequence[Sequence[str]]) -> None:
  """Add the values to a new entry in the `context` dict.

  This adds an entry to the module-level `ctx` dict with the specified `name`
  and `values`. The first entry in `fields` will be used as the key to the
  `ctx` entry and the remaining entries will be used as the keys in the
  nested-dict value. All entries in `values` must specify every field, although
  a field value may be empty. A field with an empty value will be skipped.

  For example:

    values = [
      ("key", "x", "y"),
      ("a", "b", "c"),
      ("1", "2", "",),
      ("do", "", "mi"),
    ]
   add("my_context", values)

  would result in the following:

    ctx["my_context"] = {
      "a": {
        "x": "b",
        "y": "c",
      },
      "1": {
        "x": "2",
      },
      "do": {
        "y": "mi",
      },
    }

  Args:
    name: The name of the context.
    fields: The schema for this context.
    values: The values for this context.
  """

  if name in ctx:
    raise ValueError("context '{0}' already exists".format(name))

  if len(fields) == 0:
    raise ValueError("fields cannot be empty")
  for field in fields:
    if len(fields) == 0:
      raise ValueError("field names cannot be empty")

  key, fields = fields[0], fields[1:]
  logging.info(
      "Loading context '{0}' with field '{1}' as key".format(name, key))

  data = {}
  for value in values:
    key, value = value[0], value[1:]
    if key == "":
      raise ValueError("key in context '{0}' cannot be empty".format(key))
    if len(value) != len(fields):
      raise ValueError(
          "value '{0}' in context '{1}' does not match fields '{2}'".format(
              value, key, fields))

    d = {}
    for f, v in zip(fields, value):
      # Do not set any empty fields.
      if v != "":
        d[f] = v
    data[key] = d

  logging.debug("Loaded context {0}:\n{1}".format(name, pformat(data)))

  ctx[name] = data
