# Executive Summary

This project builds a machine learning model to predict residential property prices using transaction data.

Model Performance

R²: ~0.85

MAPE: ~21%


The model explains about 85% of the variance in property prices

## Key Findings from the Data

Property size (actual area) is the most important factor.

Location (area + project) significantly affects price.

Off-plan vs ready and freehold status influence pricing but are not dominant.

Proximity to metro and malls has some impact, but not much.

Price distribution is heavily right-skewed, which justified log transformation.



# Technical Decisions
Why LightGBM?

Linear regression was tested as a baseline but underperformed due to non-linear relationships.

Neural networks were considered unnecessary for this structured dataset.

Real estate pricing relationships are non-linear. LightGBM was chosen because:

It handles non-linear interactions naturally.

It works well with structured/tabular data.


Trade-offs Considered

Accuracy vs Interpretability
SHAP were used to retain interpretability.

Accuracy vs Speed
LightGBM provides both high accuracy and fast inference.

instance_date was used for train-test split.


3. Production Readiness Assessment
Model Limitations

Data is from a limited time window (2025 only).


Expensive propertiess may have larger prediction errors.

Updated encoding mappings when new projects emerge.

Recommended Retraining Frequency

### Assumptions

If a new area or project appears:

The system maps it to the global mean encoding.

The model still generates a stable prediction.

Data is time-dependent, so sorting by INSTANCE_DATE

Transactions or unique even if they have same transaction number



# For scaling:

Deploy behind a load balancer.

Use container orchestration(K8s)

Implement monitoring and logging.
mprovements are more dependent on richer data than on more complex modeling.