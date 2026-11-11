import os
import sys

import numpy as np
import pandas as pd
import torch
from botorch.acquisition.multi_objective import qLogNoisyExpectedHypervolumeImprovement
from botorch.fit import fit_gpytorch_mll
from botorch.models import ModelListGP, SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.optim import optimize_acqf
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.utils.multi_objective.box_decompositions.dominated import (
    DominatedPartitioning,
)
from gpytorch.mlls import ExactMarginalLogLikelihood
from pandas import DataFrame
from scipy.stats.qmc import LatinHypercube, scale

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kidoe.benchmark import SnarPyrrolidineCSTRBenchmark

torch.set_default_dtype(torch.double)

N = 6
NUM_RESTARTS = 5
RAW_SAMPLES = 128
MC_SAMPLES = 64
OBJECTIVES = ['sty', 'e-factor']
seed = 12

def to_maximize(dataset):
    return torch.tensor(
        np.stack([dataset['sty'].to_numpy(), -dataset['e-factor'].to_numpy()], axis=-1)
    )


rng = np.random.default_rng(seed)
snar_prld_exp = SnarPyrrolidineCSTRBenchmark()
domain = snar_prld_exp.domain
lhc = LatinHypercube(len(domain), rng=rng)
sample = lhc.random(N)
l_bounds = [v[0] for v in domain.values()]
u_bounds = [v[1] for v in domain.values()]
dataset = DataFrame(scale(sample, l_bounds, u_bounds), columns=domain.keys())
dataset = snar_prld_exp.run_experiments(dataset)

bounds = torch.tensor([l_bounds, u_bounds])
train_x_lhs = torch.tensor(dataset[list(domain.keys())].to_numpy())
train_y_lhs = to_maximize(dataset)

ref_point = train_y_lhs.min(dim=0).values  # worst point in maximisation space, shape (2,)

hv_curve = []
train_x = train_x_lhs[:0]
train_y = train_y_lhs[:0]
for i in range(N):
    train_x = torch.cat([train_x, train_x_lhs[i:i + 1]])
    train_y = torch.cat([train_y, train_y_lhs[i:i + 1]])
    hv_curve.append(
        DominatedPartitioning(ref_point=ref_point, Y=train_y)
        .compute_hypervolume()
        .item()
    )
for i in range(N):
    models = []
    for j in range(train_y.shape[-1]):
        model = SingleTaskGP(
            train_x, train_y[:, j:j + 1],
            input_transform=Normalize(d=train_x.shape[-1], bounds=bounds),
            outcome_transform=Standardize(m=1),
        )
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        fit_gpytorch_mll(mll)
        models.append(model)
    model = ModelListGP(*models)

    sampler = SobolQMCNormalSampler(sample_shape=torch.Size([MC_SAMPLES]))
    acq = qLogNoisyExpectedHypervolumeImprovement(
        model=model,
        ref_point=ref_point,
        X_baseline=train_x,
        sampler=sampler,
        prune_baseline=True,
    )
    candidate, _ = optimize_acqf(
        acq_function=acq,
        bounds=bounds,
        q=1,
        num_restarts=NUM_RESTARTS,
        raw_samples=RAW_SAMPLES,
    )

    sug_dataset = {k: [candidate[0, idx].item()] for idx, k in enumerate(domain)}
    sug_dataset = pd.DataFrame(sug_dataset)
    new_dataset = snar_prld_exp.run_experiments(sug_dataset)
    dataset = pd.concat([dataset, new_dataset], ignore_index=True)

    new_x = torch.tensor(new_dataset[list(domain.keys())].to_numpy())
    new_y = to_maximize(new_dataset)
    train_x = torch.cat([train_x, new_x])
    train_y = torch.cat([train_y, new_y])

    hv_curve.append(DominatedPartitioning(ref_point=ref_point, Y=train_y).compute_hypervolume().item())

print(dataset)

#     pareto_mask = is_non_dominated(train_y).numpy()
#     pareto_fronts.append(dataset.loc[pareto_mask, list(domain.keys()) + OBJECTIVES])
