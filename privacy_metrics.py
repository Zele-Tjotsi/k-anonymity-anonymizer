"""
Privacy metrics for k-anonymity evaluation.
Implements l-diversity and other advanced privacy measures.
"""

import pandas as pd
import numpy as np
from collections import Counter


def compute_l_diversity(df: pd.DataFrame, quasi_columns: list, sensitive_column: str) -> dict:
    """
    Compute l-diversity for each equivalence class.
    
    l-diversity ensures each group of indistinguishable records (based on quasi-identifiers)
    has at least 'l' distinct values for the sensitive attribute.
    
    Args:
        df: Anonymized DataFrame
        quasi_columns: List of quasi-identifier column names
        sensitive_column: Name of the sensitive attribute column (e.g., Disease, Salary)
    
    Returns:
        Dictionary containing:
        - min_l_diversity: Minimum l-diversity across all groups
        - avg_l_diversity: Average l-diversity
        - groups_below_threshold: Number of groups failing a given threshold
        - details: Per-group diversity statistics
    """
    
    if sensitive_column not in df.columns:
        return {
            "error": f"Sensitive column '{sensitive_column}' not found in data",
            "min_l_diversity": 0,
            "avg_l_diversity": 0,
            "groups_below_threshold": 0,
            "details": {}
        }
    
    # Group by quasi-identifiers
    grouped = df.groupby(quasi_columns)
    
    l_diversity_values = []
    group_details = {}
    
    for group_key, group_data in grouped:
        # Get unique values of sensitive attribute in this group
        sensitive_values = group_data[sensitive_column].tolist()
        unique_values = set(sensitive_values)
        diversity = len(unique_values)
        
        # Count frequency of each value
        value_counts = Counter(sensitive_values)
        
        group_details[str(group_key)] = {
            "size": len(group_data),
            "diversity": diversity,
            "unique_values": list(unique_values),
            "value_distribution": dict(value_counts)
        }
        
        l_diversity_values.append(diversity)
    
    if not l_diversity_values:
        return {
            "error": "No equivalence classes found",
            "min_l_diversity": 0,
            "avg_l_diversity": 0,
            "groups_below_threshold": 0,
            "details": {}
        }
    
    min_diversity = min(l_diversity_values)
    avg_diversity = np.mean(l_diversity_values)
    
    # Count groups with diversity < 2 (vulnerable to homogeneity attack)
    vulnerable_groups = sum(1 for d in l_diversity_values if d < 2)
    
    return {
        "min_l_diversity": min_diversity,
        "avg_l_diversity": round(avg_diversity, 2),
        "groups_below_threshold": vulnerable_groups,
        "total_groups": len(l_diversity_values),
        "details": group_details,
        "interpretation": _interpret_l_diversity(min_diversity, vulnerable_groups, len(l_diversity_values))
    }


def _interpret_l_diversity(min_diversity: int, vulnerable_groups: int, total_groups: int) -> str:
    """Provide human-readable interpretation of l-diversity results."""
    
    if min_diversity >= 3:
        return "Strong: Each group has at least 3 distinct sensitive values. Well-protected against attribute disclosure."
    elif min_diversity == 2:
        return "Moderate: Some groups have only 2 distinct sensitive values. May be vulnerable to certain attacks."
    else:
        if vulnerable_groups == total_groups:
            return f"WARNING: All {total_groups} groups have zero diversity (only 1 sensitive value). Complete attribute disclosure possible."
        else:
            return f"WARNING: {vulnerable_groups} out of {total_groups} groups have zero diversity (only 1 sensitive value). These groups leak sensitive information."


def compute_entropy_l_diversity(df: pd.DataFrame, quasi_columns: list, sensitive_column: str) -> float:
    """
    Compute entropy-based l-diversity (stronger definition).
    Measures the entropy of sensitive values within each group.
    
    Higher entropy = better diversity.
    """
    
    import math
    
    if sensitive_column not in df.columns:
        return 0.0
    
    grouped = df.groupby(quasi_columns)
    
    entropies = []
    
    for _, group_data in grouped:
        value_counts = group_data[sensitive_column].value_counts(normalize=True)
        entropy = -sum(p * math.log2(p) for p in value_counts if p > 0)
        entropies.append(entropy)
    
    if not entropies:
        return 0.0
    
    return round(sum(entropies) / len(entropies), 3)


def check_l_diversity_threshold(df: pd.DataFrame, quasi_columns: list, sensitive_column: str, l_threshold: int = 2) -> dict:
    """
    Check if dataset meets required l-diversity threshold.
    
    Args:
        l_threshold: Minimum required distinct values per group (default 2)
    
    Returns:
        Pass/fail status and detailed results
    """
    
    diversity_result = compute_l_diversity(df, quasi_columns, sensitive_column)
    
    if "error" in diversity_result:
        return {"pass": False, "error": diversity_result["error"]}
    
    meets_threshold = diversity_result["min_l_diversity"] >= l_threshold
    
    return {
        "pass": meets_threshold,
        "min_l_diversity": diversity_result["min_l_diversity"],
        "threshold": l_threshold,
        "recommendation": _get_recommendation(diversity_result, l_threshold)
    }


def _get_recommendation(result: dict, threshold: int) -> str:
    """Generate actionable recommendations."""
    
    if result["min_l_diversity"] >= threshold:
        return "Dataset meets l-diversity requirements."
    
    if result["groups_below_threshold"] == result["total_groups"]:
        return "Critical: All groups lack diversity. Consider: (1) Adding more generalized quasi-identifiers, (2) Suppressing the sensitive column, (3) Collecting more data"
    
    return f"Some groups lack diversity. Consider: (1) Further generalization of quasi-identifiers to merge groups, (2) Bucketing sensitive values into broader categories"
