import argparse
from torchtext import datasets
from models.transformer import TextClassifier as transformerClassifier
from models.fformer import TextClassifier as fformerClassifier
from models.qfformer import TextClassifier as qfformerClassifier


parser = argparse.ArgumentParser()
parser.add_argument('-B', '--batch_size', default=32, type=int)
parser.add_argument('-E', '--n_epochs', default=10, type=int)
parser.add_argument('-l', '--lr', default=0.001, type=float)
parser.add_argument('-e', '--embed_dim', default=32, type=int)
parser.add_argument('-s', '--max_seq_len', default=256, type=int)
parser.add_argument('-f', '--ffn_dim', default=32, type=int)
parser.add_argument('-t', '--n_transformer_blocks', default=1, type=int)
parser.add_argument('-H', '--n_heads', default=2, type=int)
parser.add_argument('-q', '--n_qubits_transformer', default=5, type=int)
parser.add_argument('-Q', '--n_qubits_ffn', default=5, type=int)
parser.add_argument('-L', '--n_qlayers', default=1, type=int)
parser.add_argument('-d', '--dropout_rate', default=0.1, type=float)
args = parser.parse_args()

models = {
    'Transformer' : transformerClassifier,
    'fformer' : fformerClassifier,
    'qfformer' : qfformerClassifier,
}

datasets = {
    'IMDB': datasets.IMDB,
    'AG_NEWS': datasets.AG_NEWS,
}
