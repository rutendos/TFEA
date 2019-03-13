#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''This file contains a list of independent functions that do not call other 
    functions
'''
#==============================================================================
__author__ = 'Jonathan D. Rubin and Rutendo F. Sigauke'
__credits__ = ['Jonathan D. Rubin', 'Rutendo F. Sigauke', 'Jacob T. Stanley',
                'Robin D. Dowell']
__maintainer__ = 'Jonathan D. Rubin'
__email__ = 'Jonathan.Rubin@colorado.edu'
#==============================================================================
import pathlib
#==============================================================================
#Functions used before 'import config' statement
#==============================================================================
def make_out_directories(dirs=False, config_object=None):
    '''Creates output directories in a user-specified location where all TFEA 
        outputs will go.

    Parameters
    ----------
    dirs : boolean
        determines whether output folders will be created or not (default: 
        False)
        
    config : dict
        a configparser object that contains variables within the config file

    Returns
    -------
    output : string 
        full path to the parent output directory

    tempdir : string
        full path to the temporary directory where files are stored

    figuredir : string
        full path to the directory containing figures and plots
        
    e_and_o : string
        full path to the directory that stores stdout and stderr files
    '''
    #Output directory
    output = pathlib.Path(config_object['OUTPUT']['OUTPUT'].strip("'"))
    name = config_object['OUTPUT']['NAME'].strip("'")
    outfoldername = name
    output = output / outfoldername

    #Make parent output directory
    if dirs:
        output.mkdir(exist_ok=True)

    #Temporary files will go in this directory
    tempdir = output / 'temp_files'
    if dirs:
        tempdir.mkdir(exist_ok=True)

    #Error and out files will go in this directory
    e_and_o = output / 'e_and_o'
    if dirs:
        e_and_o.mkdir(exist_ok=True)

    #Directory where plots used in html file will be stored.
    figuredir = output / 'plots'
    if dirs:
        figuredir.mkdir(exist_ok=True)

    return output, tempdir, figuredir, e_and_o
#==============================================================================

#==============================================================================
def parse_config(srcdirectory=None, config_object=None, outputdir=None, 
                tempdir=None, figuredir=None):
    '''Creates the config.py file which is used in many aspects of TFEA. Within
        this config.py file, it writes all variables provided in the config
        parameter and also writes output, tempdir, and figuredir full paths

    Parameters
    ----------
    srcdirectory : string
        full path to TFEA source directory
        
    config : dict
        a configparser object that contains variables within the config file

    output : string 
        full path to the parent output directory

    tempdir : string
        full path to the temporary directory where files are stored

    figuredir : string
        full path to the directory containing figures and plots

    Returns
    -------
    None
    '''
    outfile =  open(srcdirectory / 'config.py','w')
    for key in config_object:
        for item in config_object[key]:
            outfile.write(item.upper()+'='+config_object[key][item]+'\n')

    outfile.write('OUTPUTDIR="'+outputdir.as_posix()+'"\n')
    outfile.write('TEMPDIR="'+tempdir.as_posix()+'"\n')
    outfile.write('FIGUREDIR="'+figuredir.as_posix()+'"\n')
    
    outfile.close()
#==============================================================================

#==============================================================================
def verify_config_file():
    '''Verifies that all necessary variables are present within the inputted 
        config file and that they are the correct variable types.
    
    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    TypeError
        When variable type does not match required type

    NameError
        When variable is not found within config
    '''
    import config

    #USER INPUTS
    #==========================================================================
    try:
        if type(config.NAME) != str:
            raise TypeError('NAME variable must be a string.')
    except NameError:
        raise NameError('NAME variable not found in config.ini file.')

    try:
        if type(config.OUTPUT) != str:
            raise TypeError('OUTPUT variable must be a string.')
    except NameError:
        raise NameError('OUTPUT variable not found in config.ini file.')

    try:
        if type(config.LABEL1) != str:
            raise TypeError('LABEL1 variable must be a string.')
    except NameError:
        raise NameError('LABEL1 variable not found in config.ini file.')

    try:
        if type(config.LABEL2) != str:
            raise TypeError('LABEL2 variable must be a string.')
    except NameError:
        raise NameError('LABEL2 variable not found in config.ini file.')

    try:
        if type(config.BED1) != list:
            raise TypeError('BED1 variable must be a list.')
    except NameError:
        raise NameError('BED1 variable not found in config.ini file.')
    
    try:
        if type(config.BED2) != list:
            raise TypeError('BED2 variable must be a list.')
    except NameError:
        raise NameError('BED2 variable not found in config.ini file.')

    try:
        if type(config.BAM1) != list:
            raise TypeError('BAM1 variable must be a list.')
    except NameError:
        raise NameError('BAM1 variable not found in config.ini file.')
    
    try:
        if type(config.BAM2) != list:
            raise TypeError('BAM2 variable must be a list.')
    except NameError:
        raise NameError('BAM2 variable not found in config.ini file.')

    #COMBINE Module
    #==========================================================================
    # try:
    #     if config.COMBINE != 'merge all' or 'tfit clean' or 'intersect/merge' or 'tfit remove small' or False:
    #         raise TypeError('Unrecognized option for COMBINE module.')
    #     elif config.COMBINE == False:
    #         try:
    #             if type(config.COMBINE_FILE) != str:
    #                 raise TypeError('COMBINE_FILE variable must be a string.')
    #         except NameError:
    #             raise NameError('COMBINE_FILE must be specified if COMBINE is'
    #                             'set to False.')
    # except NameError:
    #     raise NameError('COMBINE variable not found in config.ini file.')

    #COUNT Module
    #==========================================================================
    try:
        if type(config.COUNT) != bool:
                raise TypeError('COUNT variable must be a boolean.')
        elif config.COUNT != True:
            try:
                if type(config.COUNT_FILE) != str:
                    raise TypeError('COUNT_FILE variable must be a string.')
            except NameError:
                raise NameError('COUNT_FILE must be specified if COUNT is'
                                'set to False.')
    except NameError:
        raise NameError('COUNT variable not found in config.ini file.')



    try:
        if type(config.DESEQ) != bool:
            raise TypeError('DESEQ variable must be a boolean.')
    except NameError:
        raise NameError('DESEQ variable not found in config.ini file.')

    # try:
    #     if type(config.CALCULATE) != bool:
    #         raise TypeError('CALCULATE variable must be a boolean.')
    # except NameError:
    #     raise NameError('CALCULATE variable not found in config.ini file.')

    # try:
    #     if type(config.HOMER) != bool:
    #         raise TypeError('HOMER variable must be a boolean.')
    # except NameError:
    #     raise NameError('HOMER variable not found in config.ini file.')

    try:
        if type(config.SINGLEMOTIF) != bool and type(config.SINGLEMOTIF) != str:
            raise TypeError('SINGLEMOTIF variable must be a boolean or string.')
    except NameError:
        raise NameError('SINGLEMOTIF variable not found in config.ini file.')

    # try:
    #     if type(config.GENOMEWIDEHITS) != bool:
    #         raise TypeError('GENOMEWIDEHITS variable must be a boolean.')
    # except NameError:
    #     raise NameError('GENOMEWIDEHITS variable not found in config.ini file.')

    # try:
    #     if type(config.FIMO) != bool:
    #         raise TypeError('FIMO variable must be a boolean.')
    # except NameError:
    #     raise NameError('FIMO variable not found in config.ini file.')

    try:
        if type(config.TEMP) != bool:
            raise TypeError('TEMP variable must be a boolean.')
    except NameError:
        raise NameError('TEMP variable not found in config.ini file.')

    try:
        if type(config.PLOTALL) != bool:
            raise TypeError('PLOT variable must be a boolean.')
    except NameError:
        raise NameError('PLOT variable not found in config.ini file.')

    try:
        if type(config.METAPLOT) != bool:
            raise TypeError('METAPLOT variable must be a boolean.')
    except NameError:
        raise NameError('METAPLOT variable not found in config.ini file.')

    

    

    

    try:
        if type(config.PADJCUTOFF) != float:
            raise TypeError('PADJCUTOFF variable must be a float.')
    except NameError:
        raise NameError('PADJCUTOFF variable not found in config.ini file.')

    try:
        if type(config.LARGEWINDOW) != float:
            raise TypeError('LARGEWINDOW variable must be a float.')
    except NameError:
        raise NameError('LARGEWINDOW variable not found in config.ini file.')

    try:
        if type(config.SMALLWINDOW) != float:
            raise TypeError('SMALLWINDOW variable must be a float.')
    except NameError:
        raise NameError('SMALLWINDOW variable not found in config.ini file.')

    # if config.FIMO != True:
    #     try:
    #         if type(config.MOTIF_GENOMEWIDE_HITS) != str:
    #             raise TypeError('MOTIF_GENOMEWIDE_HITS variable must be a string.')
    #     except NameError:
    #         raise NameError('MOTIF_GENOMEWIDE_HITS variable not found in config.ini file.')
    # else:
    #     try:
    #         if type(config.FIMO_THRESH) != float:
    #             raise TypeError('FIMO_THRESH variable must be a float.')
    #     except NameError:
    #         raise NameError('FIMO_THRESH variable not found in config.ini file.')

    # if config.HOMER == True:
    #     try:
    #         if type(config.HOMER_MOTIF_FILE) != str:
    #             raise TypeError('HOMER_MOTIF_FILE variable must be a string.')
    #     except NameError:
    #         raise NameError('HOMER_MOTIF_FILE variable not found in config.ini file.')

    try:
        if type(config.GENOMEFASTA) != str:
            raise TypeError('GENOMEFASTA variable must be a string.')
    except NameError:
        raise NameError('GENOMEFASTA variable not found in config.ini file.')

    # try:
    #     if type(config.MOTIFDATABASE) != str:
    #         raise TypeError('MOTIFDATABASE variable must be a string.')
    # except NameError:
    #     raise NameError('MOTIFDATABASE variable not found in config.ini file.')

    # try:
    #     if type(config.LOGOS) != str:
    #         raise TypeError('LOGOS variable must be a string.')
    # except NameError:
    #     raise NameError('LOGOS variable not found in config.ini file.')
    
    try:
        if type(config.DPI) != float and config.DPI != None:
            raise TypeError('DPI variable must be a float or None.')
    except NameError:
        raise NameError('DPI variable not found in config.ini file.')

    print("Config file verified, all inputs present and correct type.")
#==============================================================================

#==============================================================================