import pandas as pd
import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(color_codes=True)


def plot_prediction_errors(pred, target, name, norm_pdf=False):
    """
    Visualize prediction error distribution histagram and through time period

    Parameters:
    - pred: Preidictions numpy array
    - target: Target value numpy array
    - name: Name of the prediction period
    - nomr_pdf: show norm probability distribution

    Returns:
    """

    errors = pred - target

    e_means = round(errors.mean(), 4)
    e_std = round(errors.std(), 4)

    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    hist = axs[0].hist(pd.DataFrame(errors), density=True)
    line1 = axs[0].axvline(x=e_means + e_std*1.5, color='r', linestyle='--',
                           label=f'std {e_std}')
    line2 = axs[0].axvline(x=e_means - e_std*1.5, color='r', linestyle='--')
    line3 = axs[0].axvline(x=e_means, color='g', linestyle='--',
                           label=f'mean{e_means}')

    if norm_pdf:
        x = np.linspace(norm.ppf(0.01),norm.ppf(0.99), 100)
        norm_pdf = axs[0].plot(e_means + x, norm.pdf(x), 'r-', lw=3, alpha=0.5,
                               label='norm pdf')

    axs[0].legend(handles=[line1, line3])
    axs[0].set_title(f'Errors distibution {name}')

    pd.DataFrame(errors, columns=['error']).plot(ax=axs[1])
    axs[1].set_title(f'Errors {name}')
