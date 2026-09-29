"""
Standalone Production CLI for County-Level Estimation Model (Task 8.3 & Task 9.4).
Downtown San Diego Homeless Population Analysis

Calculates countywide unsheltered homeless estimates from downtown field counts
using the Champion Policy Regime OLS model with Student's t (df=5) calibrated 95% PIs.
Strictly enforces The 4 Mandatory Public Communication Rules.
"""

import sys
import argparse
from src.utils import calculate_county_estimate
from src.config import BETA_0, BETA_1, BETA_2, STUDENT_T_CRITICAL_95, SIGMA_EPSILON


def main():
    parser = argparse.ArgumentParser(
        description="County-Level Unsheltered Homelessness Macro Estimator (Policy Regime OLS)"
    )
    parser.add_argument(
        "--downtown-count",
        type=float,
        default=985.38,
        help="Downtown monthly adjusted count (default: 985.38 for Dec 2025)",
    )
    parser.add_argument(
        "--pre-ordinance",
        action="store_true",
        help="Flag to evaluate under pre-July 2023 ordinance regime (D_post = 0)",
    )
    args = parser.parse_args()

    post_ord = not args.pre_ordinance
    res = calculate_county_estimate(args.downtown_count, post_ordinance=post_ord)

    print("\n=======================================================")
    print("COUNTYWIDE UNSHELTERED ESTIMATION MODEL (POLICY REGIME OLS)")
    print("=======================================================")
    print(f"Model Equation:    Y = {BETA_0:.2f} + {BETA_1:.4f} * X + {BETA_2:.2f} * D_post")
    print(f"Downtown Count (X):{args.downtown_count:,.2f}")
    print(f"Policy Regime:     {res['policy_context']}")
    print(f"Degrees of Freedom:df = 5 (Student's t critical = {STUDENT_T_CRITICAL_95:.4f})")
    print(f"Margin of Error:   ±{res['margin_of_error']:,.1f} individuals (approx ±35%)")
    print("-------------------------------------------------------")
    print("THE 4 PUBLIC COMMUNICATION RULES ENFORCEMENT:")
    print(f"  • Rule 1 (Raw Precision Prohibited): Raw point = {res['raw_point_estimate']:.2f}")
    print(f"  • Rule 2 (Mandatory Rounding to 100):  Point Estimate = {res['rounded_point_estimate']:,}")
    print(f"  • Rule 3 (Calibrated 95% Interval):    [{res['rounded_lower_95']:,} to {res['rounded_upper_95']:,}]")
    print(f"  • Rule 4 (Regime Disclosure):          {res['policy_context']}")
    print("-------------------------------------------------------")
    print(f"OFFICIAL PUBLIC DISPLAY TEXT: {res['public_display_text']}")
    print("=======================================================\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
