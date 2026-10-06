"""
County-Level Estimation Modeling & Validation (Task 8.3)
Downtown San Diego Homeless Population Analysis
Author: Kyaw Soe Lwin (kylwin@ucsd.edu) / Data Science Alliance

Implements, validates, and evaluates macro-level estimation models predicting
San Diego County unsheltered Point-in-Time (PIT) homelessness from Downtown San Diego
monthly counts. Features leave-one-year-out cross-validation (LOOCV), honest 95%
prediction interval uncertainty quantification, and structural policy sensitivity checks.

Restored Oct 2026 from the Task 8.3 Drive deliverable (county_estimation_model.py, 33 KB);
the repo's county_estimation_model.py is the separate Task 9.4 quick-estimate CLI.
Change from the original: the prospective scenario's downtown input is read from
data/Forecasts_12Month.csv (first forecast month) instead of being hard-coded, and the
Dec 2025 / Jan 2025 inputs are read from data/MasterCounts_Adjusted_v2.csv.
The three model-diagnostic figures (fits, LOOCV trajectories, metrics) are not regenerated
here because they do not depend on the forecast; the scenario forest plot is.

Usage: python scripts/county_estimation_build.py
"""

import os
import hashlib
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_DIR, 'data')
FIGURES_DIR = os.path.join(REPO_DIR, 'figures', 'task8_3')

MODEL_NAMES = [
    'Ratio Estimator (Pooled)',
    'Ratio Estimator (Mean of Ratios)',
    'Ordinary Least Squares (OLS)',
    'Regression with Time Trend',
    'OLS with Policy Regime Indicator',
    'Post-Ordinance Recent Ratio',
]


def compute_sha256(filepath):
    """Compute SHA-256 hash of a file for data integrity verification."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def load_data(data_dir):
    """Load paired dataset and verify integrity."""
    paired_path = os.path.join(data_dir, 'Downtown_County_PairedCounts.csv')
    hash_init = compute_sha256(paired_path)
    df = pd.read_csv(paired_path)
    # Filter to valid paired years (excluding HUD-waived 2021)
    valid_df = df.dropna(subset=['county_unsheltered']).copy().reset_index(drop=True)
    valid_df['pit_year'] = valid_df['pit_year'].astype(int)
    valid_df['t'] = valid_df['pit_year'] - 2017
    valid_df['d_post'] = (valid_df['pit_year'] >= 2024).astype(int)
    return valid_df, paired_path, hash_init


# ==============================================================================
# Model Fitting & Prediction Functions
# ==============================================================================

def predict_ratio_pooled(X_train, Y_train, X_test):
    R = np.sum(Y_train) / np.sum(X_train)
    return X_test * R, R


def predict_ratio_mean(X_train, Y_train, X_test):
    r_bar = np.mean(Y_train / X_train)
    return X_test * r_bar, r_bar


def predict_ols(X_train, Y_train, X_test):
    model = sm.OLS(Y_train, sm.add_constant(X_train)).fit()
    pred = model.predict(sm.add_constant(X_test, has_constant='add'))
    return pred.values if hasattr(pred, 'values') else pred, model


def predict_ols_trend(X_train, Y_train, t_train, X_test, t_test):
    design_tr = pd.DataFrame({'const': 1.0, 'X': X_train, 't': t_train})
    model = sm.OLS(Y_train, design_tr).fit()
    pred = model.predict(pd.DataFrame({'const': 1.0, 'X': X_test, 't': t_test}))
    return pred.values if hasattr(pred, 'values') else pred, model


def predict_ols_regime(X_train, Y_train, d_post_train, X_test, d_post_test):
    design_tr = pd.DataFrame({'const': 1.0, 'X': X_train, 'd_post': d_post_train})
    model = sm.OLS(Y_train, design_tr).fit()
    pred = model.predict(pd.DataFrame({'const': 1.0, 'X': X_test, 'd_post': d_post_test}))
    return pred.values if hasattr(pred, 'values') else pred, model


def predict_recent_ratio(X_train, Y_train, years_train, X_test):
    mask_recent = years_train >= 2024
    if np.sum(mask_recent) > 0:
        R_rec = np.sum(Y_train[mask_recent]) / np.sum(X_train[mask_recent])
    else:
        R_rec = np.sum(Y_train) / np.sum(X_train)
    return X_test * R_rec, R_rec


# ==============================================================================
# Leave-One-Year-Out Cross-Validation (LOOCV) Engine
# ==============================================================================

def run_loocv(df, predictor_col='downtown_reported_adjusted'):
    n = len(df)
    years = df['pit_year'].values
    actual_Y = df['county_unsheltered'].values
    X_vals = df[predictor_col].values
    t_vals = df['t'].values
    d_post_vals = df['d_post'].values

    predictions = {m: np.zeros(n) for m in MODEL_NAMES}
    fold_details = []

    for k in range(n):
        x_k, t_k, d_post_k, y_k = X_vals[k:k + 1], t_vals[k:k + 1], d_post_vals[k:k + 1], actual_Y[k]
        tr = np.ones(n, dtype=bool)
        tr[k] = False
        X_tr, Y_tr, t_tr, d_tr, yrs_tr = X_vals[tr], actual_Y[tr], t_vals[tr], d_post_vals[tr], years[tr]

        p_pool, _ = predict_ratio_pooled(X_tr, Y_tr, x_k)
        p_mean, _ = predict_ratio_mean(X_tr, Y_tr, x_k)
        p_ols, _ = predict_ols(X_tr, Y_tr, x_k)
        p_tr, _ = predict_ols_trend(X_tr, Y_tr, t_tr, x_k, t_k)
        p_reg, _ = predict_ols_regime(X_tr, Y_tr, d_tr, x_k, d_post_k)
        p_rec, _ = predict_recent_ratio(X_tr, Y_tr, yrs_tr, x_k)
        for name, p in zip(MODEL_NAMES, [p_pool, p_mean, p_ols, p_tr, p_reg, p_rec]):
            predictions[name][k] = p[0]

        fold_details.append({
            'loocv_fold': k + 1, 'test_year': int(years[k]), 'downtown_count': float(x_k[0]),
            'county_unsheltered_actual': float(y_k), 'pred_ratio_pooled': float(p_pool[0]),
            'pred_ratio_mean': float(p_mean[0]), 'pred_ols': float(p_ols[0]), 'pred_ols_trend': float(p_tr[0]),
            'pred_ols_regime': float(p_reg[0]), 'pred_recent_ratio': float(p_rec[0]),
        })

    metrics_summary = []
    for m in MODEL_NAMES:
        preds = predictions[m]
        errors = actual_Y - preds
        pct_errors = errors / actual_Y
        corr = np.corrcoef(actual_Y, preds)[0, 1] if np.std(preds) > 1e-6 else np.nan
        metrics_summary.append({
            'model_name': m, 'predictor_series': predictor_col, 'n_folds': n,
            'rmse': round(float(np.sqrt(np.mean(errors ** 2))), 2),
            'mae': round(float(np.mean(np.abs(errors))), 2),
            'mape_pct': round(float(np.mean(np.abs(pct_errors)) * 100.0), 2),
            'signed_bias_pct': round(float(np.mean(pct_errors) * -100.0), 2),
            'max_abs_error': round(float(np.max(np.abs(errors))), 2),
            'corr_with_actual': round(float(corr), 4) if pd.notnull(corr) else np.nan,
        })
    df_metrics = pd.DataFrame(metrics_summary)
    df_metrics['rank_rmse'] = df_metrics['rmse'].rank().astype(int)
    df_metrics['rank_mape'] = df_metrics['mape_pct'].rank().astype(int)
    df_metrics = df_metrics.sort_values(by='rmse').reset_index(drop=True)
    return pd.DataFrame(fold_details), df_metrics, predictions


# ==============================================================================
# Full-Sample Parametric Estimation & Uncertainty Quantification
# ==============================================================================

def fit_full_models_and_intervals(df, predictor_col='downtown_reported_adjusted'):
    n = len(df)
    X = df[predictor_col].values
    Y = df['county_unsheltered'].values
    t_vals = df['t'].values
    d_post_vals = df['d_post'].values
    x_bar = np.mean(X)
    ss_x = np.sum((X - x_bar) ** 2)

    R_pool = np.sum(Y) / np.sum(X)
    s_e_pool = np.sqrt(np.sum((Y - R_pool * X) ** 2) / (n - 1))

    r_i = Y / X
    r_bar = np.mean(r_i)
    s_r = np.std(r_i, ddof=1)
    s_e_mean = np.sqrt(np.sum((Y - r_bar * X) ** 2) / (n - 1))

    m_ols = sm.OLS(Y, sm.add_constant(X)).fit()
    m_tr = sm.OLS(Y, sm.add_constant(np.column_stack([X, t_vals]))).fit()
    m_reg = sm.OLS(Y, sm.add_constant(np.column_stack([X, d_post_vals]))).fit()

    mask_post = df['pit_year'] >= 2024
    X_post, Y_post = X[mask_post], Y[mask_post]
    n_post = len(X_post)
    R_post = np.sum(Y_post) / np.sum(X_post)
    s_e_post = np.sqrt(np.sum((Y_post - R_post * X_post) ** 2) / (n_post - 1))

    return {
        'ratio_pooled': {'R': R_pool, 's_e': s_e_pool, 'df': n - 1, 't_crit': stats.t.ppf(0.975, n - 1), 'x_bar': x_bar, 'n': n},
        'ratio_mean': {'r_bar': r_bar, 's_e': s_e_mean, 's_r': s_r, 'df': n - 1, 't_crit': stats.t.ppf(0.975, n - 1), 'n': n},
        'ols': {'model': m_ols, 's_e': np.sqrt(m_ols.mse_resid), 'df': n - 2, 't_crit': stats.t.ppf(0.975, n - 2),
                'x_bar': x_bar, 'ss_x': ss_x, 'n': n},
        'ols_trend': {'model': m_tr, 's_e': np.sqrt(m_tr.mse_resid), 'df': n - 3, 't_crit': stats.t.ppf(0.975, n - 3),
                      'cov': m_tr.normalized_cov_params},
        'ols_regime': {'model': m_reg, 's_e': np.sqrt(m_reg.mse_resid), 'df': n - 3, 't_crit': stats.t.ppf(0.975, n - 3),
                       'cov': m_reg.normalized_cov_params},
        'recent_ratio': {'R': R_post, 's_e': s_e_post, 'df': n_post - 1, 't_crit': stats.t.ppf(0.975, n_post - 1),
                         'x_bar': np.mean(X_post), 'n': n_post},
    }


def _interval(y_hat, se, m):
    lo, hi = y_hat - m['t_crit'] * se, y_hat + m['t_crit'] * se
    return {'point_estimate': y_hat, 'se_pred': se, 'pi_95_lower': max(0.0, lo), 'pi_95_upper': hi,
            'pi_95_lower_unbounded': lo, 'df': m['df'], 't_crit': m['t_crit']}


def compute_prediction_intervals(fm, x0, t_val=8, d_post_val=1):
    res = {}
    m = fm['ratio_pooled']
    res['Ratio Estimator (Pooled)'] = _interval(
        m['R'] * x0, m['s_e'] * np.sqrt(1 + (x0 ** 2) / (m['n'] * (m['x_bar'] ** 2))), m)
    m = fm['ratio_mean']
    res['Ratio Estimator (Mean of Ratios)'] = _interval(
        m['r_bar'] * x0, np.sqrt(m['s_e'] ** 2 + (x0 ** 2) * (m['s_r'] ** 2) / m['n']), m)
    m = fm['ols']
    res['Ordinary Least Squares (OLS)'] = _interval(
        m['model'].predict([1.0, x0])[0],
        m['s_e'] * np.sqrt(1 + 1 / m['n'] + ((x0 - m['x_bar']) ** 2) / m['ss_x']), m)
    m = fm['ols_trend']
    v = np.array([1.0, x0, t_val])
    res['Regression with Time Trend'] = _interval(m['model'].predict(v)[0], m['s_e'] * np.sqrt(1 + v @ m['cov'] @ v), m)
    m = fm['ols_regime']
    v = np.array([1.0, x0, d_post_val])
    res['OLS with Policy Regime Indicator'] = _interval(m['model'].predict(v)[0], m['s_e'] * np.sqrt(1 + v @ m['cov'] @ v), m)
    m = fm['recent_ratio']
    res['Post-Ordinance Recent Ratio'] = _interval(
        m['R'] * x0, m['s_e'] * np.sqrt(1 + (x0 ** 2) / (m['n'] * (m['x_bar'] ** 2))), m)
    return res


def plot_current_estimates_forest(current_df, figures_dir):
    """Figure 4: Forest plot showing current county estimates and calibrated 95% PIs."""
    os.makedirs(figures_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    plot_df = current_df.copy().reset_index(drop=True)
    y_pos = np.arange(len(plot_df))
    point_est = plot_df['point_estimate'].values
    lower_95 = plot_df['pi_95_lower'].values
    upper_95 = plot_df['pi_95_upper'].values
    labels = [f"{row['model_name']}\n[{row['operational_scenario']}]" for _, row in plot_df.iterrows()]
    colors = ['#38b000' if 'Regime' in r['model_name'] else ('#1d3557' if 'OLS' in r['model_name'] else '#7209b7')
              for _, r in plot_df.iterrows()]
    for i in range(len(plot_df)):
        ax.plot([lower_95[i], upper_95[i]], [y_pos[i], y_pos[i]], color=colors[i], linewidth=2.5, alpha=0.8)
        ax.plot(point_est[i], y_pos[i], marker='o', color=colors[i], markersize=8, markeredgecolor='black')
        ax.text(point_est[i], y_pos[i] + 0.22, f"{point_est[i]:.0f}", ha='center', fontsize=8.5, fontweight='bold')
        ax.text(lower_95[i], y_pos[i] - 0.22, f"{lower_95[i]:.0f}", ha='center', fontsize=7.5, color='#555555')
        ax.text(upper_95[i], y_pos[i] - 0.22, f"{upper_95[i]:.0f}", ha='center', fontsize=7.5, color='#555555')
    ax.axvline(5714, color='#d90429', linestyle='--', linewidth=1.5, alpha=0.85, label='2025 RTFH Actual PIT (5,714)')
    ax.axvline(6110, color='#fca311', linestyle=':', linewidth=1.5, alpha=0.85, label='2024 Record PIT (6,110)')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel('Estimated San Diego County Unsheltered Homeless Population', fontsize=10.5, fontweight='bold')
    ax.set_title("Current Countywide Unsheltered Estimates with Calibrated 95% Prediction Intervals\n"
                 "Student's t Uncertainty Quantification across Estimation Approaches (Task 8.3)",
                 fontsize=12, fontweight='bold', pad=15)
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    out_path = os.path.join(figures_dir, 'current_county_estimates_scenarios.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Exported: {out_path}")


def scenario_inputs():
    """Downtown inputs for the three operational scenarios, read from the current data files."""
    m = pd.read_csv(os.path.join(DATA_DIR, 'MasterCounts_Adjusted_v2.csv'))
    tot = m[(m.component == 'total') & (m.area_type == 'neighborhood')].groupby('date').total_count.sum(min_count=1)
    fc = pd.read_csv(os.path.join(DATA_DIR, 'Forecasts_12Month.csv'))
    fc = fc[fc.series == 'Overall - reported footprint'].sort_values('forecast_date').iloc[0]
    return [
        {'scenario_key': 'latest_historical_dec2025',
         'operational_scenario': 'Latest Available Monthly Historical Count (Dec 2025)',
         'downtown_count': round(float(tot['2025-12-01']), 2), 'reference_period': '2025-12-01', 't_val': 8, 'd_post_val': 1},
        {'scenario_key': 'matched_baseline_jan2025', 'operational_scenario': 'PIT-Matched Baseline Count (Jan 2025)',
         'downtown_count': round(float(tot['2025-01-01']), 2), 'reference_period': '2025-01-01', 't_val': 8, 'd_post_val': 1},
        {'scenario_key': 'prospective_jan2026',
         'operational_scenario': f"Prospective 12-Month Horizon Point Forecast ({pd.Timestamp(fc.forecast_date):%b %Y})",
         'downtown_count': float(fc.point_forecast), 'reference_period': f"{fc.forecast_date} (Task 7.4 XGBoost)",
         't_val': 9, 'd_post_val': 1},
    ]


def main():
    print("=" * 80)
    print("TASK 8.3: BUILD AND VALIDATE COUNTY-LEVEL ESTIMATION MODEL")
    print("=" * 80)
    df, paired_path, hash_init = load_data(DATA_DIR)
    print(f"[OK] Valid paired observations: N = {len(df)} years (2017-2025, excluding waived 2021)")

    df_pred_rep, df_metrics_rep, _ = run_loocv(df, predictor_col='downtown_reported_adjusted')
    print(df_metrics_rep[['rank_rmse', 'model_name', 'rmse', 'mae', 'mape_pct', 'signed_bias_pct']].to_string(index=False))
    df_pred_f6, df_metrics_f6, _ = run_loocv(df, predictor_col='downtown_fixed6_constant')
    combined_metrics = pd.concat([df_metrics_rep, df_metrics_f6], ignore_index=True)
    combined_metrics.to_csv(os.path.join(DATA_DIR, 'CountyEstimation_LOOCV_Metrics.csv'), index=False)
    df_pred_rep.to_csv(os.path.join(DATA_DIR, 'CountyEstimation_LOOCV_Predictions.csv'), index=False)

    fitted = fit_full_models_and_intervals(df, predictor_col='downtown_reported_adjusted')
    reg = fitted['ols_regime']['model']
    print(f"Champion (Policy Regime OLS): Y = {reg.params[0]:.2f} + {reg.params[1]:.4f}*X + {reg.params[2]:.2f}*D_post"
          f"   R^2 = {reg.rsquared:.4f}, adj R^2 = {reg.rsquared_adj:.4f}")

    rows = []
    for sc in scenario_inputs():
        for m_name, res in compute_prediction_intervals(fitted, sc['downtown_count'], sc['t_val'], sc['d_post_val']).items():
            rows.append({
                'scenario_key': sc['scenario_key'], 'operational_scenario': sc['operational_scenario'],
                'reference_period': sc['reference_period'], 'downtown_input_count': sc['downtown_count'],
                'model_name': m_name, 'point_estimate': round(float(res['point_estimate']), 2),
                'se_prediction': round(float(res['se_pred']), 2), 'df_residuals': int(res['df']),
                't_critical_95': round(float(res['t_crit']), 4), 'pi_95_lower': round(float(res['pi_95_lower']), 2),
                'pi_95_upper': round(float(res['pi_95_upper']), 2),
                'pi_95_width': round(float(res['pi_95_upper'] - res['pi_95_lower']), 2),
                'pi_95_lower_unbounded': round(float(res['pi_95_lower_unbounded']), 2),
            })
    df_current = pd.DataFrame(rows)
    df_current.to_csv(os.path.join(DATA_DIR, 'CountyEstimate_Current.csv'), index=False)
    print(df_current[df_current.model_name == 'OLS with Policy Regime Indicator'][
        ['scenario_key', 'downtown_input_count', 'point_estimate', 'pi_95_lower', 'pi_95_upper']].to_string(index=False))

    plot_current_estimates_forest(
        df_current[df_current['scenario_key'].isin(['latest_historical_dec2025', 'prospective_jan2026'])], FIGURES_DIR)
    assert hash_init == compute_sha256(paired_path), "Source file modified during execution!"
    print("TASK 8.3 EXECUTION COMPLETE")


if __name__ == '__main__':
    main()
