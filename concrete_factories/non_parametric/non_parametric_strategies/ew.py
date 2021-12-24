from concrete_factories.non_parametric.non_parametric_interface import InterfaceNonParametric
from common_functions.rolling_windows_validation import rolling_windows_validation
import numpy as np


class EW(InterfaceNonParametric):
    """The EW Bayesian Concrete Class that implements the Bayesian interface"""

    def __init__(self, name='Equally Weighted Strategy', lamb=0, delta=0, upper_bound=0, lower_bound=0, validation_windows=36, cv_windows=12):
        self.name = name
        self.lamb = lamb
        self.delta = delta
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.validation_windows = validation_windows
        self.cv_windows = cv_windows
        self.data = []
        self.intermediate_data = []
        self.weights = []
        self.returns = []

    def get_dimensions(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Beta initial value": self.delta
        }

    def get_all_parameters(self):
        return {
            "Strategy Name": self.name,
            "Lambda initial value": self.lamb,
            "Beta initial value": self.delta
        }

    def get_hyper_parameters(self):
        return rolling_windows_validation(self.data)


    def solve_optimization_problem(self):
        """
        Equally Weighted Strategy
        :param data_received:
        :param parameters:
        :param optimization:
        :return: It returns the optimized weights
        """
        name = 'Equally Weighted Strategy'

        (numElements, N) = self.intermediate_data.shape
        # mean and covariance

        weights = np.ones((N, 1)) * (1 / N)
        self.weights = weights

        return self.weights



