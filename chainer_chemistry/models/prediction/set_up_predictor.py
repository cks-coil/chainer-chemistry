from typing import Optional  # NOQA

import chainer  # NOQA

from chainer_chemistry.models.ggnn import GGNN
from chainer_chemistry.models.mlp import MLP
from chainer_chemistry.models.nfp import NFP
from chainer_chemistry.models.prediction.graph_conv_predictor import GraphConvPredictor  # NOQA
from chainer_chemistry.models.relgat import RelGAT
from chainer_chemistry.models.relgcn import RelGCN
from chainer_chemistry.models.rsgcn import RSGCN
from chainer_chemistry.models.schnet import SchNet
from chainer_chemistry.models.weavenet import WeaveNet


def set_up_predictor(
        method,  # type: str
        n_unit,  # type: int
        conv_layers,  # type: int
        class_num,  # type: int
        label_scaler=None,  # type: Optional[chainer.Link]
        postprocess_fn=None  # type: Optional[chainer.FunctionNode]
):
    # type: (...) -> GraphConvPredictor
    """Set up the predictor, consisting of a GCN and a MLP.

    Args:
        method (str): Method name.
        n_unit (int): Number of hidden units.
        conv_layers (int): Number of convolutional layers for the graph
            convolution network.
        class_num (int): Number of output classes.
        label_scaler (chainer.Link or None): scaler link
        postprocess_fn (chainer.FunctionNode or None):
            postprocess function for prediction.
    """
    mlp = MLP(out_dim=class_num, hidden_dim=n_unit)  # type: Optional[MLP]

    if method == 'nfp':
        print('Training an NFP predictor...')
        conv = NFP(out_dim=n_unit, hidden_dim=n_unit, n_layers=conv_layers)
    elif method == 'ggnn':
        print('Training a GGNN predictor...')
        conv = GGNN(out_dim=n_unit, hidden_dim=n_unit, n_layers=conv_layers)
    elif method == 'schnet':
        print('Training an SchNet predictor...')
        conv = SchNet(
            out_dim=class_num, hidden_dim=n_unit, n_layers=conv_layers)
        mlp = None
    elif method == 'weavenet':
        print('Training a WeaveNet predictor...')
        n_atom = 20
        n_sub_layer = 1
        weave_channels = [50] * conv_layers

        conv = WeaveNet(
            weave_channels=weave_channels,
            hidden_dim=n_unit,
            n_sub_layer=n_sub_layer,
            n_atom=n_atom)
    elif method == 'rsgcn':
        print('Training an RSGCN predictor...')
        conv = RSGCN(out_dim=n_unit, hidden_dim=n_unit, n_layers=conv_layers)
    elif method == 'relgcn':
        print('Training a Relational GCN predictor...')
        num_edge_type = 4
        conv = RelGCN(
            out_channels=n_unit, num_edge_type=num_edge_type, scale_adj=True)
    elif method == 'relgat':
        print('Training a Relational GAT predictor...')
        conv = RelGAT(out_dim=n_unit, hidden_dim=n_unit, n_layers=conv_layers)
    else:
        raise ValueError('[ERROR] Invalid method: {}'.format(method))

    predictor = GraphConvPredictor(conv, mlp, label_scaler, postprocess_fn)
    return predictor
