__author__ = 'Jonathan Rubin'

import matplotlib
matplotlib.use('Agg')
import sys
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.stats import norm
import time
# import HTSeq as hts
from config import *

def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

def run(MOTIF_FILE,ranked_center_distance_file,ranked_center_sorted_file,figuredir,logos):
    #Initiate some variables
    H = 1500.0
    h = 150.0
    ES = list()
    Eval = 0.0
    distances = list()
    ind = list()
    negatives = 0.0
    distance_sum = 0.0
    realdistance = list()
    scatterx = list()
    sigscatterx = list()
    scattery = list()
    sigscattery = list()
    logpval = list()

    #First parse file containing motif distance and region rank. Also count total negatives to be used later
    with open(ranked_center_distance_file) as F:
        for line in F:
            line = line.strip('\n').split('\t')
            distance = float(line[-1])
            pval = float(line[3])
            rank = int(line[5])
            fc = float(line[4])
            if 0 <= distance <= h:
                value = math.exp(-distance)
                distances.append(value)
                ind.append(rank)
                distance_sum += value
                if fc > 1:
                    try:
                        logpval.append(-math.log(pval,10))
                    except ValueError:
                        logpval.append(500.0)
                else:
                    try:
                        logpval.append(math.log(pval,10))
                    except ValueError:
                        logpval.append(-500.0)
                scatterx.append(rank)
                scattery.append(distance)
                if pval < PVALCUTOFF:
                    sigscatterx.append(rank)
                    sigscattery.append(distance)
            elif h < distance <= H:
                distances.append(-1)
                ind.append(rank)
                negatives += 1.0
                if fc > 1:
                    try:
                        logpval.append(-math.log(pval,10))
                    except ValueError:
                        logpval.append(500.0)
                else:
                    try:
                        logpval.append(math.log(pval,10))
                    except ValueError:
                        logpval.append(-500.0)
                scatterx.append(rank)
                scattery.append(distance)
                if pval < PVALCUTOFF:
                    sigscatterx.append(rank)
                    sigscattery.append(distance)
    
    if len(distances) == 0:
        return "no hits"        

    #actualES calculation:
    try:
        neg = -1.0/negatives
    except:
        neg = -1.0

    #1. Replace negatives values in distances with -1.0/negatives
    distances = [neg if x==-1 else x for x in distances]

    #2. Reorder list of motif distances based on rank
    distances = [x for _,x in sorted(zip(ind,distances))]

    #3. Go through distances and add appropriately to cumulative sum (ES) list
    for distance in distances:
        if distance != neg:
            Eval += distance/distance_sum
            ES.append(Eval)
        else:
            Eval += distance
            ES.append(Eval)

    #4. The enrichment score is the maximum deviation from 0
    actualES = max(ES,key=abs)

    #To get NES, first simulate 1000 permuations of region ranks
    simES = simulate(H,distances,distance_sum,neg)

    #NES is the actualES divided by the mean ES of all permutations with the same sign as actualES
    #p-value is caluclated empirically (i.e. (# of simulated ES scores larger than actualES)/(rest of simulated ES scores))
    if actualES < 0:
        simESsubset = [x for x in simES if x < 0]
        mu = np.mean(simESsubset)
        NES = -(actualES/mu)
    else:
        simESsubset = [x for x in simES if x > 0]
        mu = np.mean(simESsubset)
        NES = actualES/mu


    #This section calculates the theoretical p-value based on the mean and standard deviation of the 1000 simulations
    #The p-value is then the CDF where x = actualES. Test is two tailed, hence: min(p,1-p)
    mu = np.mean(simES)
    sigma = np.std(simES)
    p = norm.cdf(actualES,mu,sigma)
    p = min(p,1-p)

    #Plot results for significant hits while list of simulated ES scores is in memory
    # if p < FDRCUTOFF or SINGLEMOTIF != False:
    #For human:
    # os.system("scp " + logos + MOTIF_FILE.split('.bed')[0].split('HO_')[1] + "_direct.png " + figuredir)
    # os.system("scp " + logos + MOTIF_FILE.split('.bed')[0].split('HO_')[1] + "_revcomp.png " + figuredir)

    #For mouse:
    os.system("scp " + logos + MOTIF_FILE.split('.bed')[0] + "_direct.png " + figuredir)
    os.system("scp " + logos + MOTIF_FILE.split('.bed')[0] + "_revcomp.png " + figuredir)

    logpval = [x for _,x in sorted(zip(scatterx,logpval))]

    #Plots the enrichment plot which contains three subplots:
    #   1. Typical ES vs. region rank (GSEA-style)
    #   2. A scatter plot with distance to motif on y-axis and rank on x-axis
    #   3. A plot similar to GSEAs 'phenotype label' plot to show where the fc crosses 1. On the y-axis is log10(pval) (positive if
    #       fc > 1, else negative) on the x-axis is regions ranked
    F = plt.figure(figsize=(16.5,6))
    xvals = range(1,len(ES)+1)
    limits = [1,len(ES)]
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax0 = plt.subplot(gs[0])
    ax0.plot(xvals,ES,color='green')
    ax0.axhline(0, color='black',linestyle='dashed')
    ax0.set_title('Enrichment Plot: '+ MOTIF_FILE.split('.bed')[0],fontsize=14)
    ax0.set_ylabel('Enrichment Score (ES)', fontsize=10)
    ax0.tick_params(axis='y', which='both', left='on', right='off', labelleft='on')
    ax0.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    ylims = ax0.get_ylim()
    ymax = math.fabs(max(ylims,key=abs))
    ax0.set_ylim([-ymax,ymax])
    ax0.set_xlim(limits)
    ax1 = plt.subplot(gs[1])
    ax1.scatter(scatterx,scattery,edgecolor="",color="black",s=10,alpha=0.25)
    ax1.axhline(h, color='black',linestyle='dashed',alpha=0.1)
    if DRAWPVALCUTOFF != False:
        ax1.scatter(sigscatterx,sigscattery,edgecolor="",color="red",s=10)
        ax1.axvline(PVALCUTOFF,linestyle='dashed')
        ax1.text(PVALCUTOFF,H+H/10,str(PVALCUTOFF),ha='center',va='bottom')
    ax1.tick_params(axis='y', which='both', left='off', right='off', labelleft='on')
    ax1.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    ax1.set_xlim(limits)
    ax1.set_ylim([0,H])
    # ax1.yaxis.set_ticks([0,H])
    plt.yticks([0,H],['0',str(float(H)/1000.0)])
    ax1.set_ylabel('Distance (kb)', fontsize=10)
    ax2 = plt.subplot(gs[2])
    ax2.fill_between(xvals,0,logpval,facecolor='grey',edgecolor="")
    ax2.tick_params(axis='y', which='both', left='on', right='off', labelleft='on')
    ax2.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    ylim = math.fabs(max([x for x in logpval if -500 < x < 500],key=abs))
    ax2.set_ylim([-ylim,ylim])
    ax2.yaxis.set_ticks([int(-ylim),0,int(ylim)])
    ax2.set_xlim(limits)
    ax2.set_xlabel('Rank in Ordered Dataset', fontsize=14)
    ax2.set_ylabel('Rank Metric',fontsize=10)
    plt.savefig(figuredir + MOTIF_FILE.split('.bed')[0] + '_enrichment_plot.png',bbox_inches='tight')
    plt.cla()
    plt.close()

    #Plots the distribution of simulated ESs and in a red bar plots the observed ES
    F = plt.figure(figsize=(7.5,6))
    ax2 = plt.subplot(111)
    maximum = max(simES)
    minimum = min(simES)
    ax2.hist(simES,bins=100)
    width = (maximum-minimum)/100.0
    rect = ax2.bar(actualES,ax2.get_ylim()[1]-10.0,color='red',width=width*2)[0]
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., 1.05*height, 'Observed ES', ha='center', va='bottom')
    ax2.set_xlim([min(minimum,actualES)-(width*40),max(maximum,actualES)+(width*40)])
    ax2.tick_params(axis='y', which='both', left='off', right='off', labelleft='on')
    ax2.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.title('Distribution of Simulated Enrichment Scores',fontsize=14)
    ax2.set_ylabel('Number of Simulations',fontsize=14)
    ax2.set_xlabel('Enrichment Score (ES)',fontsize=14)
    plt.savefig(figuredir + MOTIF_FILE.split('.bed')[0] + '_simulation_plot.png',bbox_inches='tight')
    plt.cla()
    plt.close()





    # return [MOTIF_FILE.split('.bed')[0],actualES,NES,p,(simNESmu,simNESsigma)]
    return [MOTIF_FILE.split('.bed')[0],actualES,NES,p]

def simulate(H,distances,distance_sum,neg,N=1000):
    #Simulate 1000 permuations of region ranks
    simES = list()
    for i in range(N):
        Eval = 0.0
        maximum = 0.0
        minimum = 0.0
        #Here we actually shuffle the regions
        np.random.shuffle(distances)

        #Then we calculate an ES just like before
        for distance in distances:
            if distance != neg:
                Eval += distance/distance_sum
                if Eval > maximum:
                    maximum = Eval
            else:
                Eval += distance
                if Eval < minimum:
                    minimum = Eval
        simES.append(max(maximum,minimum,key=abs))

    return simES

def FDR(TFresults,NESlist,figuredir):
    #This function iterates through the results and calculates an FDR for each TF motif. Also creates a moustache plot.
    FDRlist = list()
    newNESlist = list()
    sigx = list()
    sigy = list()
    for i in range(len(TFresults)):
        NES = TFresults[i][2]
        PVAL = TFresults[i][3]
        # mu,sigma = TFresults[i][4]
        # if NES > 0:
        #     F = 1-norm.cdf(NES,mu,sigma)
        #     NESsubset = [x for x in NESlist if x > 0]
        #     N = len(NESsubset)
        #     Nmu = np.mean(NESsubset)
        #     Nsigma = np.std(NESsubset)
        #     D = 1-norm.cdf(NES,Nmu,Nsigma)
        #     q = (F*N)/D
        # else:
        #     F = norm.cdf(NES,mu,sigma)
        #     NESsubset = [x for x in NESlist if x < 0]
        #     N = len(NESsubset)
        #     Nmu = np.mean(NESsubset)
        #     Nsigma = np.std(NESsubset)
        #     D = norm.cdf(NES,Nmu,Nsigma)
        #     q = (F*N)/D


        #Using classical FDR calculation ((pvalue*(# hypotheses tested))/rank of p-value)
        FDR = (PVAL*len(TFresults))/float(i+1.0)
        TFresults[i].append(FDR)
        FDRlist.append(FDR)
        newNESlist.append(NES)
        if FDR < FDRCUTOFF:
            sigx.append(NES)
            sigy.append(FDR)

    #Creates a moustache plot of the global FDRs vs. NESs
    F = plt.figure()
    plt.scatter(newNESlist,FDRlist,color='black',edgecolor='')
    plt.scatter(sigx,sigy,color='red',edgecolor='')
    plt.title("TFEA Results Moustache Plot",fontsize=14)
    plt.xlabel("Normalized Enrichment Score (NES)",fontsize=14)
    plt.ylabel("False Discovery Rate (FDR)",fontsize=14)
    limit = math.fabs(max(newNESlist,key=abs))
    plt.xlim([-limit,limit])
    plt.tick_params(axis='y', which='both', left='off', right='off', labelleft='on')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.savefig(figuredir + 'TFEA_Results_Moustache_Plot.svg')
    plt.cla()

    return TFresults


