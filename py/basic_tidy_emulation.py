import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import re
sns.set_style('white')

df = sns.load_dataset('diamonds')
df.head(2)

# %% Building a method that emulates dplyr functionality for pandas data objects.

@pd.api.extensions.register_dataframe_accessor("tidy")
class TidyPandas:

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def select(self,statement):
        '''
        complete mimic of dplyr's select() function.

        [More detail needed here]
        '''
        tmp = statement.split(',') # parse sentence

        # Track variable name reassignments
        reassignments = {entry.split('=')[1].strip():entry.split('=')[0].strip() for entry in tmp if "=" in entry}
        all_columns =list(self._obj) # record all variables
        reordering = [] # parse how columns should be reordered.
        for i in tmp:
            if "=" in i:
                reordering.append(i.split("=")[0].strip())
            elif "-" in i:
                i = i.replace("-","")
                all_columns.remove(i.strip())
            elif ("*" in i):
                grab_entries = list(filter(re.compile(f"{i}").match, all_columns))
                for new_entry in grab_entries:
                    reordering.append(new_entry.strip())
            else:
                reordering.append(i.strip())

        # if only dropping variables.
        if len(reordering) == 0:
            reordering = all_columns

        return self._obj.rename(columns=reassignments).filter(reordering)


    def rename(self,statement):
        '''
        emulator for dplyr rename().

        [More detail needed here]
        '''
        tmp = statement.split(',')
        reassignments = {entry.split('=')[1].strip():entry.split('=')[0].strip() for entry in tmp}
        return self._obj.rename(columns=reassignments)


    def mutate(self, statement):
        '''
        Emulator for dplyr's mutate

        [More documentation here]
        '''
        # Parse statement and conditions
        tmp = statement.split(',')
        states = {entry.split('=')[0].strip():entry.split('=')[1].strip() for entry in tmp}
        data_handle = "self._obj."
        columns = list(self._obj)

        # Supply data handles (when need be)
        for key,val in states.items():
            for c in columns:
                if c in val:
                    val = val.replace(c,data_handle + c)
            self._obj[key] = eval(val)
            columns = list(self._obj) # Update the new columns

        return self._obj




# %% Test

def my_add(x,y):
    return x + y

(df.
 tidy.select("yy = carat,z, dd = depth, *c").
 tidy.rename("col=color").
 sample(4).
 tidy.mutate('rr = cut + "_" + col, clarity = clarity.str.title()')
 # tidy.select("clarity, rr")
)
