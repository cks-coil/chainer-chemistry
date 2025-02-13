from typing import Any  # NOQA
from typing import Dict  # NOQA
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
        postprocess_fn=None,  # type: Optional[chainer.FunctionNode]
        conv_kwargs=None  # type: Optional[Dict[str, Any]]
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
        conv_kwargs (dict): keyword args for GraphConvolution model.
    """
    mlp = MLP(out_dim=class_num, hidden_dim=n_unit)  # type: Optional[MLP]
    if conv_kwargs is None:
        conv_kwargs = {}

    if method == 'nfp':
        print('Set up NFP predictor...')
        conv = NFP(
            out_dim=n_unit,
            hidden_channels=n_unit,
            n_update_layers=conv_layers,
            **conv_kwargs)
    elif method == 'ggnn':
        print('Set up GGNN predictor...')
        conv = GGNN(
            out_dim=n_unit,
            hidden_channels=n_unit,
            n_update_layers=conv_layers,
            **conv_kwargs)
    elif method == 'schnet':
        print('Set up SchNet predictor...')
        conv = SchNet(
            out_dim=class_num,
            hidden_channels=n_unit,
            n_update_layers=conv_layers,
            **conv_kwargs)
        mlp = None
    elif method == 'weavenet':
        print('Set up WeaveNet predictor...')
        conv = WeaveNet(hidden_dim=n_unit, **conv_kwargs)
    elif method == 'rsgcn':
        print('Set up RSGCN predictor...')
        conv = RSGCN(
            out_dim=n_unit,
            hidden_channels=n_unit,
            n_update_layers=conv_layers,
            **conv_kwargs)
    elif method == 'relgcn':
        print('Set up Relational GCN predictor...')
        num_edge_type = 4
        conv = RelGCN(
            out_dim=n_unit,
            n_edge_types=num_edge_type,
            scale_adj=True,
            **conv_kwargs)
    elif method == 'relgat':
        print('Set up Relational GAT predictor...')
        conv = RelGAT(
            out_dim=n_unit,
            hidden_channels=n_unit,
            n_update_layers=conv_layers,
            **conv_kwargs)
    else:
        raise ValueError('[ERROR] Invalid method: {}'.format(method))
    # TODO (nakago): Add nfp_gwm, ggnn_gwm, rsgcn_gwm, gin_gwm

    predictor = GraphConvPredictor(conv, mlp, label_scaler, postprocess_fn)
    return predictor
