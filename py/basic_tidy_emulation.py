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

    # AUXILIARY FUNCTIONS --------------
    def unique_list(list_entry=[]):
        '''doc'''
        seen = set()
        seen_add = seen.add
        return [i for i in list_entry if not (i in seen or seen_add(i))]


    def unique_columns(d):
        '''doc'''
        return d.loc[:,~d.columns.duplicated()]


    def parse_statement(self,statement):
        '''
        Parsing method for quotation statement into dictionary for evaluation.
        '''
        open = True
        statement_cleaned = ""
        for text in statement:

            if text == "(":
                open = False
            elif text == ")":
                open = True

            if open and text == ",":
                statement_cleaned += "<::>"
            else:
                statement_cleaned += text

        tmp = statement_cleaned.split('<::>')
        states = {entry.split('=')[0].strip():entry.split('=')[1].strip() for entry in tmp}
        return states


    # DPLYR EMULATORS ---------------------------------

    def select(self,statement):
        '''
        complete mimic of dplyr's select() function.

        [More detail needed here]
        Add ... as a place holder for everything
        '''
        # Track variable name reassignments
        tmp = statement.split(',') # parse sentence
        reassignments = {entry.split('=')[1].strip():entry.split('=')[0].strip() for entry in tmp if "=" in entry}
        all_columns =list(self._obj) # record all variables
        reordering = [] # parse how columns should be reordered.
        for i in tmp:
            if "=" in i:
                reordering.append(i.split("=")[0].strip())
            elif "-" in i:
                i = i.replace("-","")
                all_columns.remove(i.strip())
            elif "*" in i:
                grab_entries = list(filter(re.compile(f"{i}").match, all_columns))
                for new_entry in grab_entries:
                    reordering.append(new_entry.strip())
            else:
                reordering.append(i.strip())

        if statement.strip()[-3:] == "...":
            for c in all_columns:
                if c not in reordering:
                    reordering.append(c)

        # if only dropping variables.
        if len(reordering) == 0:
            reordering = all_columns

        return unique_columns(self._obj.rename(columns=reassignments).filter(reordering))


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
        states = self.parse_statement(statement)
        data_handle = "self._obj."
        columns = list(self._obj)

        # Supply data handles (when need be)
        for key, val in states.items():

            for c in columns:
                if c in val:
                    val = val.replace(c,data_handle + c)
            self._obj[key] = eval(val)

            if key not in columns:
                columns.append(key) # Update the new columns

        return self._obj.filter(columns)


# %% Test

def my_add(a,b):
    return a + b


df.head(1)
(df.
 tidy.select("z, cut, color, y, depth, this = x").
 # tidy.rename("col=color").
 sample(4).
 tidy.mutate('zz = np.add(z,this), rr = cut + "_" + color').
 tidy.select("this, cut, rr, y, ...")
)



# %%



d =  pd.DataFrame(dict(A=[1,2],B=[2,3])).filter(["A","B","A"])
d

def unique_columns(d):
    return d.loc[:,~d.columns.duplicated()]
