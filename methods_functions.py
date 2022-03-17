#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Morgane T. and Ozan O.

Script of methods that we can apply to CTD and WP lists
Adapted from overlapAnalysis.py from Ozan O. (Paper Vitamin A)
"""

# Libraries
import pandas as pd
from scipy.stats import hypergeom
from statsmodels.stats.multitest import multipletests


# Functions
def overlap(targetGeneSet, WPGenesDict, WPBackgroundGenesSet, chemNames, WPDict):
    """
    Calculate overlap between target genes and Rase Diseases WP

    :param set targetGeneSet: Set of HGNC targets
    :param dict WPGenesDict: Dictionary of Rare Diseases WP
    :param set WPBackgroundGenesSet: Set of all HGNC inside WikiPathway for Homo sapiens
    # :param dict WPDict: Dictionary of WP composed of title of them

    :return:
        - **df** (*pd.DataFrame*) – Data frame of overlap metrics for each rare diseases WP
    """
    # Parameters
    # WP = "WP2059"
    WPGeneSet = set()
    WPIDs = []
    WPTitles = []
    WPsizes = []
    TargetSizes = []
    intersectionSizes = []
    universSizes = []
    pValues = []
    intersections = []

    # Calculate pvalue overlap for each RD WP found
    for WP in WPGenesDict:
        if WP != "WPID":
            WPGeneSet = set(WPGenesDict[WP])

            # M is the population size (Nb of genes inside WikiPathway for Homo sapiens pathways)
            # n is the number of successes in the population (Nb of genes inside the selected RD WP)
            # N is the sample size (Nb of genes shared between target list (from chemical) and background genes from WP)
            # x is the number of drawn “successes” (Nb of genes shared between target list and RD WP)
            M = len(WPBackgroundGenesSet)
            n = len(WPGeneSet)
            N = len(targetGeneSet.intersection(WPBackgroundGenesSet))  # Taking only genes that are also in background
            intersection = list(WPGeneSet.intersection(targetGeneSet))
            x = len(intersection)
            # print(M, n, N, x)

            # Hypergeometric test
            pval = hypergeom.sf(x - 1, M, n, N)

            WPIDs.append(WP)
            WPTitles.append(WPDict[WP])
            WPsizes.append(n)
            TargetSizes.append(N)
            intersectionSizes.append(x)
            universSizes.append(M)
            pValues.append(pval)
            intersection.sort()
            intersections.append(' '.join(intersection))

    # Multiple tests to correct pvalue
    reject, pValsAdj, alphacSidak, alphacBonf = multipletests(pValues, alpha=0.05, method='fdr_bh')

    # Final
    df = pd.DataFrame({'WPID': WPIDs,
                       'WPTitle': WPTitles,
                       'WPSize': WPsizes,
                       'TargetSize': TargetSizes,
                       'IntersectionSize': intersectionSizes,
                       'UniversSize': universSizes,
                       'pValue': pValues,
                       'pAdjusted': pValsAdj,
                       'Intersection': intersections
                       })

    # Write into a file
    df.to_csv('test/Overlap_' + chemNames + '_withRDWP.csv', ';', index=False)

    # return df


def overlapAnalysis(chemTargetsDict, WPGeneRDDict, WPBackgroundGenes,WPDict):
    """
    :param chemTargetsDict:
    :param WPGeneRDDict:
    :param WPBackgroundGenes:
    :return:
    """
    # For each chemical targets, calculate overlap with RD WP
    for chem in chemTargetsDict:
        overlap(targetGeneSet=set(chemTargetsDict[chem]),
                WPGenesDict=WPGeneRDDict,
                WPBackgroundGenesSet=set(WPBackgroundGenes),
                chemNames=chem,
                WPDict=WPDict)