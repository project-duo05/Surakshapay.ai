import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_shap_explainer(model, X_train):
    """
    Returns a SHAP explainer based on model type.
    IsolationForest is tree-based.
    OCSVM is kernel-based.
    """
    # For Isolation Forest, we can use TreeExplainer
    from sklearn.ensemble import IsolationForest
    if isinstance(model.model, IsolationForest):
        explainer = shap.TreeExplainer(model.model)
        return explainer
    else:
        # Fallback to KernelExplainer for OCSVM/LOF (can be slow, so sample)
        X_sample = shap.sample(X_train, 50)
        explainer = shap.KernelExplainer(model.model.predict, X_sample)
        return explainer

def generate_shap_summary_plot(explainer, X):
    """
    Generate SHAP summary plot as a matplotlib figure
    """
    shap_values = explainer.shap_values(X)
    
    # Set dark theme for matplotlib
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0a0e17')
    ax.set_facecolor('#0a0e17')
    
    shap.summary_plot(shap_values, X, show=False)
    
    # Clean up plot styling
    plt.tight_layout()
    return fig
