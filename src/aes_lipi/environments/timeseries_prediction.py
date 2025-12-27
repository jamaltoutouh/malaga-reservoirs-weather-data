import logging
import os
import sys

import torch


class EncoderTimeseriesPrediction(Encoder):
    """Encoder for timeseries reservoir prediction."""
    
    def __init__(self, x_dim=100, z_dim=10, width=100, height=1) -> None:
        super(EncoderTimeseriesPrediction, self).__init__(x_dim, z_dim, width, height)
        assert self.x_dim == self.height * self.width
        self.h_dim = 20  # Hidden dimension
        self.lin1 = torch.nn.Linear(self.x_dim, self.h_dim)
        self.lin2 = torch.nn.Linear(self.h_dim, self.z_dim)

    def forward(self, x):
        x = torch.nn.functional.relu(self.lin1(x))
        x = torch.nn.functional.relu(self.lin2(x))
        return x

    def encode(self, x):
        h = self.forward(x)
        return h


class VariationalEncoderTimeseriesPrediction(Encoder):
    """Variational encoder for timeseries reservoir prediction."""
    
    def __init__(self, x_dim=100, z_dim=10, width=100, height=1) -> None:
        super(VariationalEncoderTimeseriesPrediction, self).__init__(
            x_dim, z_dim, width, height
        )
        self.h_dim = 20

        self.fc1 = torch.nn.Linear(self.x_dim, self.h_dim)
        self.fc21 = torch.nn.Linear(self.h_dim, self.z_dim)
        self.fc22 = torch.nn.Linear(self.h_dim, self.z_dim)

    def encode(self, x):
        h = torch.nn.functional.relu(self.fc1(x))
        mu = self.fc21(h)
        log_var = self.fc22(h)
        return mu, log_var


class DecoderTimeseriesPrediction(Decoder):
    """Decoder for timeseries reservoir prediction."""
    
    def __init__(self, x_dim=100, z_dim=10, width=100, height=1) -> None:
        super(DecoderTimeseriesPrediction, self).__init__(x_dim, z_dim, width, height)
        assert self.x_dim == self.height * self.width
        self.h_dim = 20
        self.lin1 = torch.nn.Linear(self.z_dim, self.h_dim)
        self.lin2 = torch.nn.Linear(self.h_dim, self.x_dim)

    def forward(self, x):
        x = torch.nn.functional.relu(self.lin1(x))
        x = torch.nn.functional.sigmoid(self.lin2(x))
        return x

    def decode(self, z):
        x_p = self.forward(z)
        return x_p


class VariationalDecoderTimeseriesPrediction(DecoderTimeseriesPrediction):
    """Variational decoder for timeseries reservoir prediction."""
    
    def __init__(self, x_dim=100, z_dim=10, width=100, height=1) -> None:
        super(VariationalDecoderTimeseriesPrediction, self).__init__(
            x_dim, z_dim, width, height
        )


class AutoencoderTimeseriesPrediction(Autoencoder):
    """Autoencoder for timeseries reservoir prediction using MSE loss."""
    
    def __init__(self, encoder, decoder):
        super(AutoencoderTimeseriesPrediction, self).__init__(encoder, decoder)
        self.L2_loss = torch.nn.MSELoss()

    def loss_function(self, x_p, x) -> torch.Tensor:
        L2 = self.L2_loss(x_p, x)
        self.encoder.loss = L2.data.item()
        self.decoder.loss = L2.data.item()
        return L2


class VariationalAutoencoderTimeseriesPrediction(VariationalAutoencoder):
    """Variational autoencoder for timeseries reservoir prediction."""
    
    def loss_function(self, x_p, x, mu, log_var):
        x_p = torch.clamp(x_p, max=1.0)
        inf_mask = torch.isinf(x_p)
        if inf_mask.any():
            logging.warning("Inf in reconstruction")

        nan_mask = torch.isnan(x_p)
        if nan_mask.any():
            logging.warning("Nan in reconstruction")
            x_p = torch.nan_to_num(x_p, nan=1.0)

        x_p = torch.clamp(x_p, min=0.0, max=1.0)
        BCE = torch.nn.functional.binary_cross_entropy(x_p, x, reduction="sum")
        KLD = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        loss = BCE + KLD
        nan_mask = torch.isnan(loss)
        if nan_mask.any():
            logging.warning("Nan in loss")
            loss = torch.nan_to_num(loss, nan=10000000)

        return loss

