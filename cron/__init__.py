def is_tor_exit_node(input):
    import urllib
    import urllib.request
    import numpy as np
    import pandas as pd
    df = pd.read_csv('/home/vagrant/work/projects/chipwhisperer/jupyter/TORIPS.csv', header = None)
    N= len(df)
    for i in range(N):
        if df.values[i] == input:
            output = 1
            break
        else:
            output = 0
        return output
