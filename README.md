# Generation of Nonlinear Parameter Space
The sure independence screening and sparsifying operator (SISSO) algorithm was published in 2018 by Ouyang et. al. This algorithm inspired this "SISSO-ish" code for application of nonlinear parameters to linear modeling techniques.

## What does this code do?
### 1. Data Cleaning
   1.1. Drop non-numerical columns and any designated to skip
   
   1.2. Remove colinear parameters from input data set
### 2. Nonlinear Parameter Generation
   2.1. Perform algebraic transformations on data set
   
   2.2. Evaluate transformed parameters for p-value improvment from parent parameters
   
   2.3. Save evaluated parameters and concatenate to original data set.
   
   2.4. Repeat from 2.1. for iterations (iter=int)
### 3. Export Transformed and Original Parameters

## Example Usage

# Publications:
- Original paper: R. Ouyang, S. Curtarolo, E. Ahmetcik, M. Scheffler, and L. M. Ghiringhelli, Phys. Rev. Mater. 2, 083802 (2018).
- Original repository: https://github.com/rouyang2017/SISSO.git

Our Implementation:
- Souza, L. W.§, Miller, B. R. §, Cammarota, R. C., Lo, A., Lopez, I., Shiue, Y. S., Bergstrom, B. S., Fettinger, J., Sigman, M., Shaw, J. T. Deconvoluting Nonlinear Catalyst-Substrate Effects in the Intramolecular Dirhodium-Catalyzed C-H Insertion of Donor/Donor Carbenes Using Data Science Tools. ACS Catalysis, 2024, 14(1), 104–115. https://doi.org/10.1021/acscatal.3c04256
