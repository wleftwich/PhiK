import functools

import pandas as pd

from . import phik as phik_phik
from . import binning
from . import significance
from . import outliers


class PhikDataFrame(pd.DataFrame):
    hist2d = binning.hist2d
    phik_matrix = phik_phik.phik_matrix
    global_phik = phik_phik.global_phik_array
    significance_matrix = significance.significance_matrix
    outlier_significance_matrices = outliers.outlier_significance_matrices
    outlier_significance_matrix = outliers.outlier_significance_matrix


class PhikSeries(pd.Series):
    hist2d = binning.hist2d_from_array
    outlier_significance_matrix = outliers.outlier_significance_from_array


def phik_df(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return PhikDataFrame(f(*args, *kwargs))
    return wrapper


def phik_series(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return PhikSeries(f(*args, *kwargs))
    return wrapper

