# SISSO-inspired algorithm for the propogation of nonlinear parameter space
# Original publication for SISSO algorithm:
#   R. Ouyang, S. Curtarolo, E. Ahmetcik, M. Scheffler, and L. M. Ghiringhelli, Phys. Rev. Mater. 2, 083802 (2018).
# SISSO Repository:
#   https://github.com/rouyang2017/SISSO.git
#
# Developer: Beck Miller (beck.miller@utah.edu)

import sys
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import permutation_test_score
from sklearn.linear_model import LinearRegression

class PARAMS():
    def __init__(self):
        PARAMS.all_par = None
        PARAMS.clean_par = None
        PARAMS.y_values = None
        PARAMS.p_values = None

        PARAMS.iter = 2 # massive time scale here!
        PARAMS.colin_cut = 0.7
        PARAMS.eval_p = False
    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'colin_cut':
                PARAMS.colin_cut = value
            elif key == 'eval_p':
                PARAMS.eval_p = value
            elif key == 'iter':
                PARAMS.iter = value

def check_stats_all():
    # check R2 of generated parameter against saved set
    #   (saves if R2 < colin_cut)
    corr = pd.corr(PARAMS.all_par, method=r2_score)
    drop_cols = []
    for col in corr:
        if corr[col].max(axis=1) >= PARAMS.colin_cut:
            drop_cols.append(col)
    PARAMS.all_par.drop(columns=drop_cols, in_place=True)
    PARAMS.clean_par = PARAMS.all_par

    if PARAMS.eval_p:
        PARAMS.p_values = {}
        for col in PARAMS.all_par:
            score, permutation_scores, pvalue = permutation_test_score(LinearRegression(), x[col1], PARAMS.y_values, random_state=42)
            PARAMS.p_values[col] = pvalue
    # check p-value of generated parameter against saved set
    #   (saves if pvalue < parent pvalue(s))

def check_stats_parents(x, df):

    parent_pvalues = []
    for col in df:
        score, permutation_scores, pvalue = permutation_test_score(LinearRegression(), df[col], PARAMS.y_values, random_state=42)
        parent_pvalues.append(pvalue)

    drop_cols = []
    for col in x:
        score, permutation_scores, pvalue = permutation_test_score(LinearRegression(), x[col], PARAMS.y_values, random_state=42)
        if pvalue > parent_pvalues:
            drop_cols.append(col)

    x.drop(columns=drop_cols, in_place=True)

    return x

def generate_biv_params():
    '''
    Perform bivariate functions on parmeter set. Parameters are kept
    if their p-value is lower than p-values of both parent parameters.
        returns DataFrame of new parameters

    Functions:
        - add(_+_)
        - subtract (_-_)
        - mult (_*_)
        - divide (_/_)
    '''
    add_pars = pd.DataFrame({})
    for col1 in PARAMS.clean_par:
        for col2 in PARAMS.clean_par:
            x = {}
            x1 = PARAMS.clean_par[col1]
            x2 = PARAMS.clean_par[col2]
            # domain violations can be skipped
            try:
                x[col1+'_/_'] = x1/x2
            except:
                pass
            x[col1+'_+_'] = x1+x2
            x[col1+'_*_'] = x1*x2
            x[col1+'_-_'] = x1-x2

            x = check_stats_parents(x, PARAMS.clean_par[[col1, col2]])
            add_pars.append(x)

    PARAMS.clean_par = pd.DataFrame(add_pars)

def generate_univ_params():
    '''
    Perform univariate functions on parmeter set. Parameters are kept
    if their p-value is lower than p-value of the parent parameter.
        returns DataFrame of new parameters

    Functions:
        - square root (_sqrt)
        - cube root (_cubrt)
        - natural log (_ln)
        - inverse (_1/)
        - exponential e (_e^)
        - squared (_^2)
        - cubed (_^3)
    '''
    add_pars = []
    for col in PARAMS.clean_par:
        x = {}
        # domain violations can be skipped
        try:
            x[col+'_sqrt'] = np.sqrt(x)
        except:
            pass
        try:
            x[col+'_cubrt'] = x**(1/3)
        except:
            pass
        try:
            x[col+'_ln'] = np.log(x)
        except:
            pass
        try:
            x[col+'_1/'] = 1/x
        except:
            pass
        x[col+'_e^'] = np.exp(x)
        x[col+'_^2'] = x**2
        x[col+'_^3'] = x**3

        x = check_stats_parents(x, PARAMS.clean_par[col])
        add_pars.append(x)

    PARAMS.clean_par = pd.DataFrame(add_pars)

def command_center(inp, colin_cut=0.7, eval_p=False, y_col=None, ignore_cols=None):
    '''
    Calls other functions and exports final parameters to cvs
        inp = input csv file (string)
        colin_cut = colinearity cut off for initial cleaning and addition criteria (float)
        eval_p = evaluate p-values in cleaning steps, on/off (boolean, default: False)
                    - if True y_col is required
        y_col = column name for y values
        ignore_cols = list of column names to ignore (list, default: None)
    '''
    # intitialize run parameters
    par = PARAMS()
    par.set_params(self, colin_cut=colin_cut, eval_p=eval_p)
    # read input parameter file (csv)
    df = pd.read_csv(inp)
    par.y_values = df[y_col]
    # drop non-numerical or undesired columns
    if ignore_cols:
        par.all_par.drop(columns=ignore_cols+[y_col], in_place=True)
    else:
        par.all_par.drop(columns=y_col, in_place=True)
    par.all_par = df
    # clean colinear input params
    check_stats_all()

    for i in range(par.iter):
        p_1 = generate_univ_params()
        p_2 = generate_biv_params()

        if not p_1.empty and not p_2.empty:
            p = p_1.merge(p_2, lefton_index=True, righton_index=True)
        elif not p_1.empty and p_2.empty:
            p = p_1
        elif p_1.empty and not p_2.empty:
            p = p_2
        else:
            print('something went wrong!')
            continue

        if not p.empty:
            par.clean_par = par.clean_par.merge(p, lefton_index=True, righton_index=True)
    par.clean_par.to_csv(file.split('.')[0]+'_out.csv')

if __name__ == '__main__':
    if len(ys.argv) > 1:
        command_center(sys.argv[1])
    else:
        print('please specify an input cvs file')
        sys.exit()
