from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO
from common_functions.rolling_windows_validation import rolling_windows_validation
import numpy as np


class InitialConfiguration:
    def initial_configuration(self, strategy, params):
        if strategy == 'WUBC':
            #optim_param = {'lambda_value': ('cont', [0, 1]), 'upperBound': ('cont', [0, 1])}
            optim_param = params
        if strategy == 'WLBC':
            param_hip = {'lambda_value': ('cont', [0, 1]), 'lowerBound': ('cont', [0, 1])}
        if strategy == 'CustomStrategy':
            for x, y in params.items():
                if x!='f' and x!='hp':
                    exec('self.{}=params["{}"]'.format(x, x))
            #self.validation_windows=params['validation_windows']
            param_hip = params['hp']
            self.optim_param = params['hp']
        if strategy != 'CustomStrategy':
            param_hip = params
            self.optim_param = params





        # Create the validation set
        self.intermediate_data = self.data[0:-self.validation_windows:, :]
        # Compute the CV windows
        # Create the optimization variable

        sexp = squaredExponential()
        gp = GaussianProcess(sexp)
        acq = Acquisition(mode='ExpectedImprovement')
        #param = {'lambda_value': ('cont', [0, 1]), 'upperBound': ('cont', [0, 1])}

        # param es equivalente en MATLAB a:
        #   num = WUBC.obj.lambda_value
        #   ub = WUBC.obj.upperBound
        # Bayesian optimization:



        """'lambda_value1º
        'lambda_value2'
        'lambda_value3'"""
        #param_hip = {'lambda_value': ('cont', [0, 1]), 'upperBound': ('cont', [0, 1])}


        def errorLoss(*args, **kwards):
            for x,y in kwards.items():
                self.optim_param.setdefault(x,y)
                self.values = kwards
            rolling_windows_validation(self)
            value = np.std(self.returns) / self.returns.mean()
            return value

        results = GPGO(gp, acq, errorLoss, param_hip)
        try:
            results.run(max_iter=1)
        except TypeError:
            pass
        # Extract the best parameters
        # obj.lambda_value = results.best[[0]]
        # obj.upperBound = results.best[[1]]
        self.values = results.getResult()

        for x, y in dict(self.values[0]).items():
            exec('self.{}={}'.format(x,y))
        # obj.lambda_value = results.getResult()
        # obj.upperBound = 0.3128
        return 'SUCCESS'

