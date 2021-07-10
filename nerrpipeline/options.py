import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class NERRPipelineOptions(PipelineOptions):

  @classmethod
  def _add_argparse_args(cls, parser):  # type: (_BeamArgumentParser) -> None
    parser.add_argument("input_file", default="gs://environmental_data/landing_zone/*.csv")
    parser.add_argument("output_file", default="gs://environmental_data/structured_zone/output.csv")
