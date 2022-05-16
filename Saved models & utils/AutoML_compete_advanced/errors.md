## Error for 2_Xgboost

bad allocation
Traceback (most recent call last):
  File "D:\Anaconda\envs\cancer\lib\site-packages\supervised\base_automl.py", line 1087, in _fit
    trained = self.train_model(params)
  File "D:\Anaconda\envs\cancer\lib\site-packages\supervised\base_automl.py", line 372, in train_model
    mf.train(results_path, model_subpath)
  File "D:\Anaconda\envs\cancer\lib\site-packages\supervised\model_framework.py", line 233, in train
    learner.fit(
  File "D:\Anaconda\envs\cancer\lib\site-packages\supervised\algorithms\xgboost.py", line 200, in fit
    self.model = xgb.train(
  File "D:\Anaconda\envs\cancer\lib\site-packages\xgboost\core.py", line 532, in inner_f
    return f(**kwargs)
  File "D:\Anaconda\envs\cancer\lib\site-packages\xgboost\training.py", line 181, in train
    bst.update(dtrain, i, obj)
  File "D:\Anaconda\envs\cancer\lib\site-packages\xgboost\core.py", line 1733, in update
    _check_call(_LIB.XGBoosterUpdateOneIter(self.handle,
  File "D:\Anaconda\envs\cancer\lib\site-packages\xgboost\core.py", line 203, in _check_call
    raise XGBoostError(py_str(_LIB.XGBGetLastError()))
xgboost.core.XGBoostError: bad allocation


Please set a GitHub issue with above error message at: https://github.com/mljar/mljar-supervised/issues/new

