#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.


from pydantic import BaseConfig
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from zenml.config import DockerSettings
from zenml.integrations.constants import (
    AWS,
    EVIDENTLY,
    KUBEFLOW,
    KUBERNETES,
    MLFLOW,
    SKLEARN,
    SLACK,
)
from zenml.model_registries.base_model_registry import ModelVersionStage

PIPELINE_SETTINGS = dict(
    docker=DockerSettings(
        required_integrations=[
            AWS,
            EVIDENTLY,
            KUBEFLOW,
            KUBERNETES,
            MLFLOW,
            SKLEARN,
            SLACK,
        ],
    )
)

DEFAULT_PIPELINE_EXTRAS = dict(notify_on_success=True, notify_on_failure=True)


class MetaConfig(BaseConfig):
    pipeline_name_training = "e2e_example_training"
    pipeline_name_batch_inference = "e2e_example_batch_inference"
    mlflow_model_name = "e2e_example_model"
    target_env = ModelVersionStage.STAGING
    supported_models = {
        "LogisticRegression": {
            "class": RandomForestClassifier,
            "search_grid": dict(
                criterion=["gini", "entropy"],
                max_depth=[2, 4, 6, 8, 10, 12],
                min_samples_leaf=range(1, 10),
                n_estimators=range(50, 500, 25),
            ),
        },
        "DecisionTreeClassifier": {
            "class": DecisionTreeClassifier,
            "search_grid": dict(
                criterion=["gini", "entropy"],
                max_depth=[2, 4, 6, 8, 10, 12],
                min_samples_leaf=range(1, 10),
            ),
        },
    }
    default_model_config = {
        "class": DecisionTreeClassifier,
        "params": dict(
            criterion="gini",
            max_depth=5,
            min_samples_leaf=3,
        ),
    }
