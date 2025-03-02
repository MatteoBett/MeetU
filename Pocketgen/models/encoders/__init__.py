from .cftfm import BilevelEncoder, HierEncoder, GET
from .gnn import GNN_graphpred, MLP, WeightGNN


def get_encoder(config, device):
    if config.name == 'tf':
        return HierEncoder(
            hidden_channels = config.hidden_channels,
            edge_channels = config.edge_channels,
            key_channels = config.key_channels,
            num_heads = config.num_heads,
            num_interactions = config.num_interactions,
            k = config.knn,
            cutoff = config.cutoff,
        )
    elif config.name == 'hierGT':
        return BilevelEncoder(
            hidden_channels = config.hidden_channels,
            edge_channels = config.edge_channels,
            key_channels = config.key_channels,
            num_heads = config.num_heads,
            num_interactions = config.num_interactions,
            k = config.knn,
            cutoff = config.cutoff,
            device = device
        )
    elif config.name == 'GET':
        return GET(
            hidden_channels = config.hidden_channels,
            edge_channels = config.edge_channels,
            key_channels = config.key_channels,
            num_heads = config.num_heads,
            num_interactions = config.num_interactions,
            k = config.knn,
            cutoff = config.cutoff,
            device = device
        )
    else:
        raise NotImplementedError('Unknown encoder: %s' % config.name)