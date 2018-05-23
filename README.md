TFEA
====
# Transcription Factor Enrichment Analysis
  
```
python src/ --help
usage: python src/ --config CONFIG.ini [--sbatch email@address.com]

Transcription Factor Enrichment Analysis (TFEA) takes as input a configuration
file (.ini) and outputs a folder containing TFEA results.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  REQUIRED. A configuration file containing .ini suffix (ex.
                   config.ini). See example in the examples folder.
  --sbatch SBATCH  OPTIONAL. Submits an sbatch job. If specified, input an
                   e-mail address.
 ```
 
# Table of Contents
<A href="#Requirements">Requirements</A>
<br></br>
<A href="#configparser">	confipgarser</A>

 
<H2 id="Requirements">Requirements</H1>

Before running TFEA, make sure you have the following installed on your machine:
<div style="padding-left: 50px">
  <H3 id="configparser">configparser</H3>
  TFEA uses python's configparser. If this is not installed on your machine use pip to install it:

  ```
  pip install configparser
  ```

  If you're on FIJI (CU Boulder), pip can be used to install packages to your home directory:

  ```
  pip install --user configparser
  ```
  *Note:* Here 'user' is an argument and does not mean you should replace that with your specific user ID (i.e. just copy paste this command to your terminal and don't edit anything)
</div>

  ### DESeq2
  Make sure DESeq2 is installed on your system R, in your terminal:
    
  ```
  R
  >source("https://bioconductor.org/biocLite.R")
  >biocLite("DESeq2")
  ```



## The CONFIG.ini file
Below is a brief description of each variable required in the config.ini file. These variables can be in any order under any headings but they are organized in this way for clarity. This file and a simple version without comments is also available within the examples folder.

  ```bash
  #Example config.ini file for use with TFEA. Contains full descriptions of all variables.

  [MODULES]
  #Which parts of TFEA would you like to run? These are switches to turn on/off different modules in TFEA

  #This module combines bed files from BED and merges them using bedtools. If False, it will assume BEDS[0] contains the bed file of interest (must be a sorted bed file). (boolean)
  COMBINE = True

  #This module performs bedtools multicov which requires bam files and a bed file. It will count reads for each bam file across all regions in the inputted bed file. (boolean)
  COUNT = True

  #This module performs DESeq and then ranks regions based on the p-value obtained from DESeq, if you set this to false, TFEA will look for the DESeq file within your specified output directory. (boolean)
  DESEQ = True

  #This module performs the bulk of the calculation of TFEA and will most likely take the longest. Unless you just want to generate files, this should usually be set to True. (boolean)
  CALCULATE = True

  #Determines whether ES calculations will be run in parallel. This is recommended to speed up the process.       (boolean)
  POOL=True

  #This module draws dots on enrichment scatter plot based on whether they are less than the specified p-value cutoff. (boolean)
  DRAWPVALCUTOFF = False

  #This module allows you to specify whether you want to perform TFEA for all motifs in the specified database or whether you want to do just one motif. If you want to do a single motif, you must specify the exact name of the motif (ex. SINGLEMOTIF = 'HO_SP3_HUMAN.H10MO.B.bed'). (boolean)
  SINGLEMOTIF = False

  [DATA]
  #Full path to where you want the data to be output. TFEA outputs a folder with results. (string)
  OUTPUT = './'

  #A variable that can be used if wanted. This variable can be referenced later on using ${BEDDIR} (optional string)
  BEDDIR = '/full/path/to/BEDS/'

  #A list of full paths to BED files corresponding to all treatments. One or multiple BED files can be used but they MUST be within a list. (list of strings)
  BEDS = [${BEDDIR}+'BEDNAME1.bed',${BEDDIR}+'BEDNAME2.bed']

  #A variable that can be used if wanted. This variable can be referenced later on using ${BAMDIR} (optional string)
  BAMDIR = '/full/path/to/BAMS/'

  #A list of full paths to sorted BAM files corresponding to treatment 1. (list of strings)
  BAM1 = [${BAMDIR}+'CONDITION1_rep1.sorted.bam',${BAMDIR}+'CONDITION1_rep2.sorted.bam']

  #The name of treatment 1. (string)
  LABEL1 = 'Treatment 1'

  #A list of full paths to sorted BAM files corresponding to treatment 2. (list of strings)
  BAM2 = [${BAMDIR}+'CONDITION2_rep1.sorted.bam',${BAMDIR}+'CONDITION2_rep2.sorted.bam']

  #The name of treatment 2. (string)
  LABEL2 = 'Treatment 2'


  [THRESHOLDS]
  #FDR cut off for calling significant hits (float)
  FDRCUTOFF = 0.1

  #P-value cut off for calling significant hits (float)
  PVALCUTOFF = 0.1

  #Corresponds to the furthest motif hits that will be displayed in the enrichment scatter plot. This does not affect results (float)
  LARGEWINDOW = 1500.0

  #Corresponds to the threshold in which a positive or negative hit is called. Changing this parameter will change your results, only change if you have a good reason to do so. (float)
  SMALLWINDOW = 150.0
  ```



## Running on local machine
If you desire to run TFEA on your local machine, make sure you have the following programs installed:

  python/2.7.14
  
  bedtools/2.25.0
  
  python/2.7.14/matplotlib/1.5.1
  
  python/2.7.14/scipy/0.17.1
  
  python/2.7.14/htseq/0.9.1
  
  samtools/1.3.1
  
  meme/4.12.0

Python packages can be installed using pip, others may require additional installation steps.

Once these packages are installed, TFEA can be run using:

  ```bash
  python src/ --config CONFIG.ini
  ```



## Using SBATCH
Submitting jobs through the slurm scheduler is supported. To use this module:

  ```bash
  python src/ --config CONFIG.ini --sbatch email@address.com
  ```


Node configuration can be changed within scripts/run_main.sbatch. See here the sbatch code used:

  ```qsub
  #!/bin/bash

  ###Name the job
  #SBATCH --job-name=TFEA

  ###Specify the queue
  #SBATCH -p short

  ###Specify WallTime
  #SBATCH --time=24:00:00

  ### Specify the number of nodes/cores
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  ### Allocate the amount of memory needed
  #SBATCH --mem=500gb

  ### Set error and output locations. These will be automatically updated to the output directory.
  #SBATCH --error /scratch/Users/user/e_and_o/%x.err
  #SBATCH --output /scratch/Users/user/e_and_o/%x.out

  ### Set your email address. This is changed automatically
  #SBATCH --mail-type=ALL
  #SBATCH --mail-user=jonathan.rubin@colorado.edu

  ### Load required modules
  module purge
  module load python/2.7.14
  module load bedtools/2.25.0
  module load python/2.7.14/matplotlib/1.5.1
  module load python/2.7.14/scipy/0.17.1
  module load python/2.7.14/htseq
  module load samtools/1.3.1
  module load meme/4.12.0

  ### now call your program

  python ${src} --config ${config} --sbatch SUBMITTED
  ```
**NOTE:** For TFEA to properly run a job, the python call within the sbatch script:
>python ${src} --config ${config} --sbatch SUBMITTED

**MUST NOT BE CHANGED**
