TidyPandas
================

As a devoted follower of `tidy` data principles, `pandas` often feels
slugish, convoluted, and considerably less elegant than the `tidyverse`
suite of packages in `R`. This repository is a (progressively emerging)
Rosetta Stone of tidy principles using pandas. This repository is merely
my “ah-ha\!”s that I’ve collected over the years as I translate
`tidyverse`-methods to python’s `pandas`. “Ah-ha\!”s that I tend to
forget, so I’ve opted to write them down.

We’re all in this together, so if you have any
suggestions/corrections/comments, please send them along. This is
<u>currently a work in progress</u>.I’ll add to it as I remember things
(or don’t and need to re-remember, which is more the norm these days\!).

> Note: There are already useful cheatsheets out there: see
> [here](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) and
> [here](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PandasPythonForDataScience.pdf)
> (for instance).

## Quick Comparison

<center>

**Main Data Wrangling
Functions**

</center>

|    `dplyr`    |     `pandas`     | Description                                                               |
| :-----------: | :--------------: | ------------------------------------------------------------------------- |
|  `select()`   |   `.filter()`    | select column variables                                                   |
|  `rename()`   |   `.rename()`    | rename column variables                                                   |
|  `filter()`   |    `.query()`    | row-wise subset of a data frame by a values of a column variable          |
|  `mutate()`   |   `.assign()`    | Create a new variable on the existing data frame                          |
|  `arrange()`  | `.sort_values()` | Arrange all data values along a specified (set of) column variable(s)     |
| `group_by()`  |   `.groupby()`   | Index data frame by specific (set of) column variable(s) value(s)         |
| `summarize()` |     `.agg()`     | aggregate data by specific function rules                                 |
|     `%>%`     |       `()`       | piping, fluid programming, or the passing one function output to the next |

<center>

**Subordinate Data Wrangling Functions**

</center>

|     `dplyr`     |       `pandas`        | Description |
| :-------------: | :-------------------: | ----------- |
| `starts_with()` | `.filter(regex="^w")` |             |
|  `ends_with()`  | `.filter(regex="w$")` |             |

## Applied Examples

The examples will all show a `tidy`way of performing a specific task
(using the `tidyverse`) and then doing so with its `pandas` equivalent.
Let’s load in the necessary packages/modules.

<img src='Figures/R_logo.png' width="25">

``` r
require(tidyverse)
```

    FALSE Warning: package 'tibble' was built under R version 3.5.2

    FALSE Warning: package 'stringr' was built under R version 3.5.2

<img src='Figures/py_logo.png' width="25">

``` python
import pandas as pd
import numpy as np 
```

> Note that I pass data back and forth in an `R` instance using
> [`reticulate`](https://rstudio.github.io/reticulate/), so any
> `r.<call>` is the `R` instance in the python environment that allows
> one to pull data between realms.

### Data

For the below examples, I’ll use the `gapminder` data from the
[`gapminder`
package](https://cran.r-project.org/web/packages/gapminder/index.html).

<img src='Figures/R_logo.png' width="25">

``` r
dat = gapminder::gapminder
dat %>% head(2) # R version
```

    FALSE # A tibble: 2 x 6
    FALSE   country     continent  year lifeExp     pop gdpPercap
    FALSE   <fct>       <fct>     <int>   <dbl>   <int>     <dbl>
    FALSE 1 Afghanistan Asia       1952    28.8 8425333      779.
    FALSE 2 Afghanistan Asia       1957    30.3 9240934      821.

<img src='Figures/py_logo.png' width="25">

``` python
print(r.dat.head(2)) # Python Version
```

    FALSE        country continent  year  lifeExp      pop   gdpPercap
    FALSE 0  Afghanistan      Asia  1952   28.801  8425333  779.445314
    FALSE 1  Afghanistan      Asia  1957   30.332  9240934  820.853030

### `select()`

<img src='Figures/R_logo.png' width="25">

``` r
dat %>% 
  select(country) %>% 
  head(2)
```

    FALSE # A tibble: 2 x 1
    FALSE   country    
    FALSE   <fct>      
    FALSE 1 Afghanistan
    FALSE 2 Afghanistan

<img src='Figures/py_logo.png' width="25">

``` python
print(
r.dat
.filter(['country'])
.head(2)
)
```

    FALSE        country
    FALSE 0  Afghanistan
    FALSE 1  Afghanistan

### `select(contains())`

<img src='Figures/R_logo.png' width="25">

``` r
dat %>% 
  select(contains("p")) %>% 
  head(2)
```

    FALSE # A tibble: 2 x 3
    FALSE   lifeExp     pop gdpPercap
    FALSE     <dbl>   <int>     <dbl>
    FALSE 1    28.8 8425333      779.
    FALSE 2    30.3 9240934      821.

<img src='Figures/py_logo.png' width="25">

``` python
print(
r.dat
.filter(regex="p")
.head(2)
)
```

    FALSE    lifeExp      pop   gdpPercap
    FALSE 0   28.801  8425333  779.445314
    FALSE 1   30.332  9240934  820.853030

### `select(starts_with())`

<img src='Figures/R_logo.png' width="25">

``` r
dat %>% 
  select(starts_with("p")) %>% 
  head(2)
```

    FALSE # A tibble: 2 x 1
    FALSE       pop
    FALSE     <int>
    FALSE 1 8425333
    FALSE 2 9240934

<img src='Figures/py_logo.png' width="25">

``` python
print(
r.dat
.filter(regex="^p")
.head(2)
)
```

    FALSE        pop
    FALSE 0  8425333
    FALSE 1  9240934

### `select(ends_with())`

<img src='Figures/R_logo.png' width="25">

``` r
dat %>% 
  select(ends_with("p")) %>% 
  head(2)
```

    FALSE # A tibble: 2 x 3
    FALSE   lifeExp     pop gdpPercap
    FALSE     <dbl>   <int>     <dbl>
    FALSE 1    28.8 8425333      779.
    FALSE 2    30.3 9240934      821.

<img src='Figures/py_logo.png' width="25">

``` python
print(
r.dat
.filter(regex="p$")
.head(2)
)
```

    FALSE    lifeExp      pop   gdpPercap
    FALSE 0   28.801  8425333  779.445314
    FALSE 1   30.332  9240934  820.853030
