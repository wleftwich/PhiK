# flake8: noqa
from .version import version as __version__

from . import phik_pandas

# array functions
from .phik import phik_from_array
from .significance import significance_from_array
from .outliers import outlier_significance_from_array

# dataframe functions
from .phik import phik_matrix, global_phik_array
from .significance import significance_matrix
from .outliers import outlier_significance_matrices, outlier_significance_matrix
