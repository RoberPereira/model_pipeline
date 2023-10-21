import numpy as np
import pandas as pd

from scipy import stats
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             r2_score, mean_absolute_percentage_error)


def compute_evaluation_metrics(y_value, y_pred, model_name='model'):
    # Calculate RMSE
    rmse = round(np.sqrt(mean_squared_error(y_value, y_pred)), 2)

    # Calculate MSE
    mse = round(mean_squared_error(y_value, y_pred), 2)

    # Calculate R-squared (R^2) score
    r2 = round(r2_score(y_value, y_pred), 2)

    # Calculate Mean Absolute Error (MAE)
    mae = round(mean_absolute_error(y_value, y_pred), 2)

    # Calculate Mean Absolute Percentage Error
    mape = round(mean_absolute_percentage_error(y_value, y_pred), 2)

    data = {model_name: {'RMSE': rmse, 'MSE': mse, 'R^2': r2,
                         'MAE': mae, 'MAPE': mape}}
    return pd.DataFrame.from_dict(data)


def compute_prediction_intervals(pred, target, confidence_level=0.95, se=None):

    """
    Compute prediction intervals
    Parameters:
    - pred
    - target
    - confidence_level
    - se
    Returns:
    - DataFrame with Lower & Upper bound
    """
    # Standar Error
    if (se is None):
        se = round(np.sqrt(mean_squared_error(target, pred)), 2)

    # Calculate the Z-score for the given confidence level
    # (This is asuming norm dist. Errors dont have)
    # z = norm.ppf((1 + confidence_level) / 2)
    # Calculate the lower and upper bounds of the prediction interval
    lower_bound = pred - (1+confidence_level) * se
    upper_bound = pred + (1+confidence_level) * se

    return pd.concat([pd.DataFrame(lower_bound)
                      .rename(columns={pred.name: f'{pred.name}_low_b'}),
                      pd.DataFrame(upper_bound)
                      .rename(columns={pred.name: f'{pred.name}_upp_b'})],
                     axis=1)


def interpolate_prediction_days(y_pred_day, dt_forecast_idx,
                                targets_day_periods, forecast_col='forecast'):
    """
    Interpolate missing days of predictions
    Parameters:
    - y_pred_day_T numpy.array: predictions array
    - dt_forecast_idx numpy.array: Dates index for forecast days
    Returns:
    - ds_m DataFrame: forecast predictions with interpolation values
    """
    ds_y = pd.DataFrame(y_pred_day.T, columns=[forecast_col],
                        index=np.take(dt_forecast_idx.to_numpy(),
                                      np.array(targets_day_periods) - 1))

    ds_m = pd.DataFrame([None for i in range(1, len(dt_forecast_idx) + 1)],
                        columns=[forecast_col], index=dt_forecast_idx)

    ds_m.loc[ds_y.index] = ds_y
    ds_m = ds_m.reset_index()

    missing_days_mask = np.delete(np.array(ds_m.index),
                                  (np.array(targets_day_periods) - 1))

    a = np.interp(np.array(ds_m.iloc[missing_days_mask].index),
                  np.array(ds_m.iloc[np.array(targets_day_periods) - 1].index),
                  np.array(ds_m.iloc[np.array(targets_day_periods) - 1]
                           [forecast_col]).astype(float))

    ds_m.loc[missing_days_mask, forecast_col] = a
    ds_m.set_index('index', inplace=True)

    return ds_m


def perform_ks_test(dist):
    kstest_result = stats.kstest(dist, 'norm')

    # Extract the test statistic and p-value
    ks_statistic, p_value = kstest_result

    # Define your significance level (alpha)
    alpha = 0.05

    # Print the results
    print(f"KS Statistic: {ks_statistic:.4f}")
    print(f"P-Value: {p_value:.4f}")

    # Determine whether to reject the null hypothesis
    if p_value < alpha:
        print("Reject the null hypothesis: Data is not normally distributed.")
    else:
        print("""Fail to reject the null hypothesis:
              Data appears to be normally distributed.""")
