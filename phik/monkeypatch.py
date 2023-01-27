"""Project: PhiK - correlation analyzer library

Module: phik.decorators.pandas

Created: 2018/11/14

Description:
    Decorators for pandas DataFrame objects

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import warnings
import pandas as pd

warnings.warn("Monkeypatching pandas.DataFrame and pandas.Series")

# add function to create a 2d histogram
from phik.binning import hist2d, hist2d_from_array
pd.DataFrame.hist2d = hist2d
pd.Series.hist2d = hist2d_from_array

# add phik correlation matrix function
from phik.phik import phik_matrix, global_phik_array
pd.DataFrame.phik_matrix = phik_matrix
pd.DataFrame.global_phik = global_phik_array

# add significance matrix function for variable dependencies
from phik.significance import significance_matrix
pd.DataFrame.significance_matrix = significance_matrix

# outlier matrix
from phik.outliers import outlier_significance_matrices, outlier_significance_matrix, outlier_significance_from_array
pd.DataFrame.outlier_significance_matrices = outlier_significance_matrices
pd.DataFrame.outlier_significance_matrix = outlier_significance_matrix
pd.Series.outlier_significance_matrix = outlier_significance_from_array
