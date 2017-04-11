import pandas as pd
import numpy as np
from multiprocess import Pool

from toolkit import *

def multicore_dataframe_row_apply(df, apply_function, num_cores=2, num_partitions=2):
    df_split = np.array_split(df, num_partitions)
    print("DF Apply with {num_cores} on {num_partitions}".format(num_cores=num_cores, num_partitions=num_partitions), label="Pandas Tools", color=print_colors.PURPLE)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(lambda x: x.apply(apply_function(x), axis=1), df_split))
    pool.close()
    pool.join()
    print("Done...", label="Pandas Tools", color=print_colors.PURPLE)
    return df
