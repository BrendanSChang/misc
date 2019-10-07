"""TODO: comment
"""

import argparse
from glob import glob
import logging
import os
import sys
from typing import Any, List, Mapping, Sequence, Tuple

import context
import resolver

'''
class ReportGenerator:
  """TODO: comment
"""

  def __init__(self, template_path: str, output_path: str):
    """TODO: comment
"""
    self.output = load_workbook(template_path)
    self.output_path

  def write(self, values: Mapping[Sequence[Tuple[int, int]], Any]):
    """TODO: comment
"""
    for (c, r), v in values:
      self.output.worksheets[0][c][r].value = v

  def save(self):
    """TODO: comment
"""
    self.output.save(self.output_path)
'''


def run(
    output_dir: str,
    context_dir: str,
    mappings: Sequence[str],
):
  # Load context.
  if context_dir is not None:
    for context_path in glob("{0}/*.csv".format(context_dir)):
      contents = resolver.load_file(context_path)
      values = [
          [value.strip() for value in row.split(",")]
          for row in contents
      ]
      context.add(os.path.split(context_path)[1], values[0], values[1:])

  # Execute mappings.
  for mapping in mappings:
    r = resolver.Resolver(resolver.load_file(mapping))
    r.resolve()


if __name__ == "__main__":
  # Set up CLI.
  parser = argparse.ArgumentParser(prog="Report Generator")
  parser.add_argument("--output_dir", default=".",
                      help="The output directory where the output will be "
                           "written, e.g. path/to/output/dir. Default is the "
                           "current directory.")
  parser.add_argument("--context_dir",
                      help="Path to the context directory. All .csv files in "
                           "this directory will automatically be loaded as a "
                           "context with the file name as the name of the "
                           "context.")
  parser.add_argument("--mapping", nargs="*", default=[],
                      help="Path to the mapping file, "
                           "e.g. path/to/mapping.mapcfg.")
  parser.add_argument("-v", "--verbose", dest="log_level", nargs="?",
                      default=logging.INFO, const=logging.DEBUG,
                      help="Enable debug logging.")
  args = parser.parse_args()

  # Set up logging.
  logging.basicConfig(
      format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
      level=args.log_level)

  # Validate command-line arguments.
  try:
    if not os.path.isdir(args.output_dir):
      raise ValueError(
          "output directory '{0}' does not exist".format(args.output_dir))

    if args.context_dir is not None and not os.path.isdir(args.context_dir):
      raise ValueError(
          "context directory '{0}' does not exist".format(args.context_dir))

    for arg in args.mapping:
      if arg[-7:] != ".mapcfg":
        raise ValueError(
            "--mapping '{0}' must specify a .mapcfg file".format(arg))
  except Exception as e:
    logging.exception("failed to parse command-line arguments: {0}".format(e))
    sys.exit(1)

  # Generate report.
  try:
    run(args.output_dir, args.context_dir, args.mapping)
  except Exception as e:
    logging.exception("failed to generate report: {0}".format(e))
