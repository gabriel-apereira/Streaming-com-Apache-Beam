import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import window

serviceAccount = r'C:\Users\gabri\Desktop\Udemy\Apache GCP\dataflow-beam-voos-b1227139fe6e.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

pipeline_options = {
    'project': 'dataflow-beam-voos',
    'runner': 'DataflowRunner',
    'region': 'southamerica-east1',
    'staging_location': 'gs://apache_beam_voos/temp',
    'temp_location': 'gs://apache_beam_voos/temp',
    'template_location': 'gs://apache_beam_voos/template/streaming_tumbling',
    'save_main_session': True,
    'streaming': True}

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)
p1 = beam.Pipeline(options=pipeline_options)


subscription = 'projects/dataflow-beam-voos/subscriptions/MeusVoos-Sub'
saida = 'projects/dataflow-beam-voos/topics/saida'


class separar_linhas(beam.DoFn):
    def process(self, record):
        return [record.decode("utf-8").split(',')]


class filtro(beam.DoFn):
    def process(self, record):
        if int(record[8]) > 0:
            return [record]


pcollection_entrada = (
    p1 | 'Read from pubsub topic' >> beam.io.ReadFromPubSub(
        subscription=subscription)
)

Tempo_Atrasos = (
    pcollection_entrada
    | "Separar por Vírgulas Atraso" >> beam.ParDo(separar_linhas())
    | "Pegar voos com atraso" >> beam.ParDo(filtro())
    | "Criar par atraso" >> beam.Map(lambda record: (record[4], int(record[8])))
    | "Window" >> beam.WindowInto(window.SlidingWindows(10, 5))
    | "Somar por key" >> beam.CombinePerKey(sum)
)

Qtd_Atrasos = (
    pcollection_entrada
    | "Separar por Vírgulas Qtd" >> beam.ParDo(separar_linhas())
    | "Pegar voos com Qtd" >> beam.ParDo(filtro())
    | "Criar par Qtd" >> beam.Map(lambda record: (record[4], int(record[8])))
    | "Window Atr" >> beam.WindowInto(window.SlidingWindows(10, 5))
    | "Contar por key" >> beam.combiners.Count.PerKey()
)

tabela_atrasos = (
    {'Qtd_Atrasos': Qtd_Atrasos, 'Tempo_Atrasos': Tempo_Atrasos}
    | "join Atrasos e Qtd" >> beam.CoGroupByKey()
    | 'Converting to byte String' >> beam.Map(lambda row: (''.join(str(row)).encode('utf-8')))
    | "Escrever no Tópico" >> beam.io.WriteToPubSub(saida)
)

result = p1.run()
result.wait_until_finish()
