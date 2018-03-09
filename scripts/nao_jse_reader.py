#!/usr/bin/env python
#-*- coding:utf-8 -*

import csv
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

rt_summary_rright = []
rt_summary_rleft = []
rt_summary_rright_sright = [] 
rt_summary_rright_sleft = []
rt_summary_rleft_sright = []
rt_summary_rleft_sleft = []
rt_summary_compatible = []
rt_summary_incompatible = []

rt_all_combined = []
rt_all_r_combined = []
rt_all_l_combined = []
rt_all_compatible = []
rt_all_incompatible = []

robot_pos = dict()
rt = dict()
offsets = dict()
rt_stim_l = dict()
rt_stim_r = dict()
rt_compatible = dict()
rt_incompatible = dict()
err = dict()
nr_trials = dict()
outlier = dict()
compatiblity = dict()
excluded = dict()

cond_l_rt = []
cond_r_rt = []

datadict = dict()

def cb_optlists(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def check_index(array, index):
    try:
        len(array[index])           
    except IndexError:
        array.append([])  

def outlier_removal(rts, curr_id, offset, compatibility):
 
    mean = rts.mean()
    std = rts.std()
    rej = ALLOWED_STD * std;
    
    compatible_outliers = 0
    incompatible_outliers = 0
    
    i = 0
    to_delete = []
    for index, elem in enumerate(rts):
        if elem > mean + rej or elem < mean - rej:
            if compatibility[index]:
                compatible_outliers += 1
            else:
                incompatible_outliers += 1
            print elem
            outlier[curr_id] += 1 
            to_delete.append(index)
            i += 1

    print "detected " + str(outlier[curr_id]) + " outliers. compatible/incompatible " + str(compatible_outliers) +"/"+ str(incompatible_outliers)
    return np.delete(rts, to_delete)
            
def fill_arrays(rts, offsets, curr_id):
   
    for index, _rt in enumerate(rts):          
        _offset = offsets[index]
        if robot_pos[curr_id] == 'right':
            if(_offset == 'right'):
                rt_stim_r[curr_id] = np.append(rt_stim_r[curr_id], _rt)
                rt_incompatible[curr_id] = np.append(rt_incompatible[curr_id], _rt)
            else:
                rt_stim_l[curr_id] = np.append(rt_stim_l[curr_id], _rt)
                rt_compatible[curr_id] = np.append(rt_compatible[curr_id], _rt)
        else:
            if(_offset == 'left'):
                rt_stim_l[curr_id] = np.append(rt_stim_l[curr_id], _rt)
                rt_incompatible[curr_id] = np.append(rt_incompatible[curr_id], _rt)
            else:
                rt_stim_r[curr_id] = np.append(rt_stim_r[curr_id], _rt)
                rt_compatible[curr_id] = np.append(rt_compatible[curr_id], _rt)
        
    assert(len(rt_incompatible[curr_id]) + len(rt_compatible[curr_id]) == len(rt[curr_id]))
    assert(len(rt_stim_r[curr_id]) + len(rt_stim_l[curr_id]) == len(rt[curr_id]))
    
        
def summarize(curr_id, remove_outliers = False):

        global rt_all_compatible
        global rt_all_incompatible    
        global rt_summary_rright
        global rt_summary_rright_sright
        global rt_summary_rright_sleft
        global rt_summary_rleft
        global rt_summary_rleft_sright
        global rt_summary_rleft_sleft
        global rt_summary_compatible
        global rt_summary_incompatible
        
        if remove_outliers:                
            rt[curr_id] = outlier_removal(rt[curr_id], curr_id, offsets[curr_id], compatiblity[curr_id])

        fill_arrays(rt[curr_id], offsets[curr_id], curr_id)
        
        error_rate = err[curr_id] / float(nr_trials[curr_id])
               
        print curr_id
        print rt[curr_id]
        print "# trials: "+ str(len(rt[curr_id])) + "(w. robot trials: " +str(nr_trials[curr_id])+")" 
        print "# compatible trials: "+ str(len(rt_compatible[curr_id]))
        print "# incompatible trials: "+ str(len(rt_incompatible[curr_id]))
        print "μ: "+str(rt[curr_id].mean())
        print "μ compatible: "+str(rt_compatible[curr_id].mean())
        print "μ incompatible: "+str(rt_incompatible[curr_id].mean())
        print "var: " +str(rt[curr_id].var())
        print "stddev: " +str(rt[curr_id].std())
        print "errors (%): " +str(err[curr_id]) + "(" +str(error_rate)+")"
        print "outliers: " +str(outlier[curr_id])
        print '################################'
        
        excluded[curr_id] = False
        
        if error_rate > ALLOWED_ERR:
            print "!!! high error detected - excluding from data set !!!"
            excluded[curr_id] = True
            return
        
        if EXCLUSION_LIST != None and curr_id in EXCLUSION_LIST:
            print "!!! id in exclusion list - excluding from data set !!!"
            excluded[curr_id] = True
            return
        
        if(robot_pos[curr_id] == 'right'):
            i = 0
            for elem in rt[curr_id]:
                check_index(cond_r_rt, i)    
                cond_r_rt[i] = np.append(cond_r_rt[i], elem)
                i +=1
            rt_summary_rright = np.append(rt_summary_rright, rt[curr_id])
            rt_summary_rright_sright = np.append(rt_summary_rright_sright, rt_stim_r[curr_id])
            rt_summary_rright_sleft = np.append(rt_summary_rright_sleft, rt_stim_l[curr_id])
        else:
            i = 0
            for elem in rt[curr_id]:
                check_index(cond_l_rt, i)    
                cond_l_rt[i] = np.append(cond_l_rt[i], elem)
                i +=1
            rt_summary_rleft = np.append(rt_summary_rleft, rt[curr_id])
            rt_summary_rleft_sright = np.append(rt_summary_rleft_sright, rt_stim_r[curr_id])
            rt_summary_rleft_sleft = np.append(rt_summary_rleft_sleft, rt_stim_l[curr_id])              
        
        rt_summary_compatible = np.append(rt_summary_compatible, rt_compatible[curr_id])
        rt_summary_incompatible = np.append(rt_summary_incompatible, rt_incompatible[curr_id])
        
        assert(len(rt_compatible[curr_id]) + len(rt_incompatible[curr_id]) == len(rt[curr_id]))
        
        i = 0
        for elem in rt_compatible[curr_id]:
            check_index(rt_all_compatible, i)    
            rt_all_compatible[i] = np.append(rt_all_compatible[i], elem)
            i += 1
            
        i = 0
        for elem in rt_incompatible[curr_id]:
            check_index(rt_all_incompatible, i)             
            rt_all_incompatible[i] = np.append(rt_all_incompatible[i], elem)
            i += 1
            
        i = 0
        for elem in rt_stim_r[curr_id]:
            check_index(rt_all_r_combined, i)
            rt_all_r_combined[i] = np.append(rt_all_r_combined[i], elem)
            i += 1
            
        i = 0
        for elem in rt_stim_l[curr_id]:
            check_index(rt_all_l_combined, i)
            rt_all_l_combined[i] = np.append(rt_all_l_combined[i], elem)
            i += 1
            
        i = 0
        for elem in rt[curr_id]:
            check_index(rt_all_combined, i)           
            rt_all_combined[i] = np.append(rt_all_combined[i], elem)
            i += 1


def read_file(filename):
    
    remove_outliers = False

    with open(filename, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        #for row in datareader:
        #    print ', '.join(row)
        firstrow = next(datareader)
        row_idx = dict()
        i = 0
        for elem in firstrow:
            row_idx[elem] = i
            i += 1
            
        #print datadict
        #print next(datareader)
            
        #while True:
         #row = next(datareader)
         #print row[row_idx['participant_id']]
        i = 0
        j = 0
        total_ids = 0
        curr_id = ''
        
        for row in datareader:
            #print row
            #print curr_id
            if (curr_id != row[row_idx['participant_id']]):                
                if (curr_id != ''): 
                    summarize(curr_id, remove_outliers)
                curr_id = row[row_idx['participant_id']]
                rt[curr_id] = []
                offsets[curr_id] = []
                compatiblity[curr_id] = []
                
                rt_stim_l[curr_id] = []
                rt_stim_r[curr_id] = []
                rt_compatible[curr_id] = []
                rt_incompatible[curr_id] = []
                
                err[curr_id] = 0
                outlier[curr_id] = 0
                nr_trials[curr_id] = 0
                
                i = 0
                j = 0
                total_ids += 1
                
            if(row[row_idx['trial_type']] == 'citk-single-stim'):
                nr_trials[curr_id] +=1
                if(row[row_idx['response']] == 'go' and row[row_idx['correct']] == 'true'):                   
                    _rt = float(row[row_idx['rt']])
                    _offset = row[row_idx['offset']]
                    
                    if robot_pos[curr_id] == _offset:
                        _comp = False
                    else:
                        _comp = True
                    
                    #if(_rt > 1000.0):
                    #    outlier[curr_id] += 1 
                    #   print "outlier analysis" + str(datadict[(curr_id, i-1)])
                    #else: 
                    
                    #data[curr_id] = np.append(rt[curr_id], row[row_idx['']] 
                    rt[curr_id] = np.append(rt[curr_id], _rt)
                    offsets[curr_id] = np.append(offsets[curr_id], _offset)
                    compatiblity[curr_id] = np.append(compatiblity[curr_id], _comp)
                        
                if(row[row_idx['correct']] == 'false'):
                    err[curr_id] += 1
                            
            #assert((len(rt_stim_l[curr_id]) + len(rt_stim_r[curr_id])) == len(rt[curr_id]))
                   
            if(row[row_idx['trial_type']] == 'button-response'):
                if curr_id not in robot_pos:
                    robot_pos[curr_id] = 'right' if row[row_idx['button_pressed']] == '0' else 'left' 
               
            datadict[(curr_id, i)] = row
            i += 1
    
    summarize(curr_id, remove_outliers) #summarize the last element
    
    print "all: " +str(len(rt_all_combined))
    print "length compatible: " + str(len(rt_all_compatible))
    print "length incompatible: " + str(len(rt_all_incompatible))
    
    assert(len(rt_summary_rleft) == len(rt_summary_rleft_sright) + len(rt_summary_rleft_sleft))
    assert(len(rt_summary_rright) == len(rt_summary_rright_sright) + len(rt_summary_rright_sleft))

def write_file(filename):
    
    with open(filename, 'w') as csvfile:
        fieldnames = ['id', 'robot_position', 
                    'rt_mean_total', 'rt_var_total', 'rt_sd_total', 
                    'rt_mean_left', 'rt_var_left', 'rt_sd_left', 
                    'rt_mean_right', 'rt_var_right', 'rt_sd_right',
                    'rt_mean_compatible', 'rt_var_compatible', 'rt_sd_compatible', 
                    'rt_mean_incompatible', 'rt_var_incompatible', 'rt_sd_incompatible', 
                    'delta', 'outlier_cnt', 'error_rate', 'excluded']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        for key in rt.keys():
            writer.writerow({
            'id': key, 'robot_position': robot_pos[key],
            'rt_mean_total': "{:.3f}".format(rt[key].mean()), 
            'rt_mean_left': "{:.3f}".format(rt_stim_l[key].mean()), 
            'rt_mean_right': "{:.3f}".format(rt_stim_r[key].mean()), 
            'rt_mean_compatible': "{:.3f}".format(rt_compatible[key].mean()), 
            'rt_mean_incompatible': "{:.3f}".format(rt_incompatible[key].mean()), 
            'delta': "{:.3f}".format(rt_compatible[key].mean() - rt_incompatible[key].mean()),
            'rt_var_total': "{:.3f}".format(rt[key].var()), 
            'rt_sd_total': "{:.3f}".format(rt[key].std()),
            'rt_var_left': "{:.3f}".format(rt_stim_l[key].var()), 
            'rt_sd_left': "{:.3f}".format(rt_stim_l[key].std()),
            'rt_var_right': "{:.3f}".format(rt_stim_r[key].var()), 
            'rt_sd_right': "{:.3f}".format(rt_stim_r[key].std()),
            'rt_var_compatible': "{:.3f}".format(rt_compatible[key].var()), 
            'rt_sd_compatible': "{:.3f}".format(rt_compatible[key].std()),
            'rt_var_incompatible': "{:.3f}".format(rt_incompatible[key].var()), 
            'rt_sd_incompatible': "{:.3f}".format(rt_incompatible[key].std()),
            'error_rate': "{:.3f}".format(err[key] / float(nr_trials[key])),
            'excluded': excluded[key]
            #'outlier_cnt': outlier[key]
            })

#            writer.writerow({
#            'id': key, 'robot_position': robot_pos[key], 'stimulus': 'left',
#            'rt_mean_total': "{:.3f}".format(rt_stim_l[key].mean()), 
#            'rt_var_total': "{:.3f}".format(rt_stim_l[key].var()), 
#            'rt_sd_total': "{:.3f}".format(rt_stim_l[key].std()),
#            })
#            
#            writer.writerow({
#            'id': key, 'robot_position': robot_pos[key], 'stimulus': 'right',
#            'rt_mean_total': "{:.3f}".format(rt_stim_r[key].mean()), 
#            'rt_var_total': "{:.3f}".format(rt_stim_r[key].var()), 
#            'rt_sd_total': "{:.3f}".format(rt_stim_r[key].std()),
#            })
                    
        writer.writerow({
            'robot_position': 'right', 
            'rt_mean_total': "{:.3f}".format(rt_summary_rright.mean()),   
            'rt_var_total': "{:.3f}".format(rt_summary_rright.var()), 
            'rt_sd_total': "{:.3f}".format(rt_summary_rright.std()),
            'rt_mean_left': "{:.3f}".format(rt_summary_rright_sleft.mean()),  
            'rt_var_left': "{:.3f}".format(rt_summary_rright_sleft.var()), 
            'rt_sd_left': "{:.3f}".format(rt_summary_rright_sleft.std()),        
            'rt_mean_right': "{:.3f}".format(rt_summary_rright_sright.mean()),       
            'rt_var_right': "{:.3f}".format(rt_summary_rright_sright.var()), 
            'rt_sd_right': "{:.3f}".format(rt_summary_rright_sright.std()), 
            'delta': "{:.3f}".format(rt_summary_rright_sleft.mean() - rt_summary_rright_sright.mean())
        })
        
        writer.writerow({
            'robot_position': 'left', 
            'rt_mean_total': "{:.3f}".format(rt_summary_rleft.mean()),   
            'rt_var_total': "{:.3f}".format(rt_summary_rleft.var()), 
            'rt_sd_total': "{:.3f}".format(rt_summary_rleft.std()),
            'rt_mean_left': "{:.3f}".format(rt_summary_rleft_sleft.mean()),  
            'rt_var_left': "{:.3f}".format(rt_summary_rleft_sleft.var()), 
            'rt_sd_left': "{:.3f}".format(rt_summary_rleft_sleft.std()),        
            'rt_mean_right': "{:.3f}".format(rt_summary_rleft_sright.mean()),       
            'rt_var_right': "{:.3f}".format(rt_summary_rleft_sright.var()), 
            'rt_sd_right': "{:.3f}".format(rt_summary_rleft_sright.std()), 
            'delta': "{:.3f}".format(rt_summary_rleft_sleft.mean() - rt_summary_rleft_sright.mean())
        })
        
        writer.writerow({
            'robot_position': 'compatible', 
            'rt_mean_total': "{:.3f}".format(rt_summary_compatible.mean()),   
            'rt_var_total': "{:.3f}".format(rt_summary_compatible.var()), 
            'rt_sd_total': "{:.3f}".format(rt_summary_compatible.std()),
            'delta': "{:.3f}".format(rt_summary_compatible.mean() - rt_summary_incompatible.mean()),
        })
        
        writer.writerow({
            'robot_position': 'incompatible', 
            'rt_mean_total': "{:.3f}".format(rt_summary_incompatible.mean()),   
            'rt_var_total': "{:.3f}".format(rt_summary_incompatible.var()), 
            'rt_sd_total': "{:.3f}".format(rt_summary_incompatible.std()),
        })
        
def plot_ids(filename,ids):

    plt.figure(figsize=(20,10))

    plt.clf()

    plt.axis([0,256, 0.0,1000.0])
    ax = plt.gca()
    ax.set_autoscale_on(False)

    for idx in ids:
        plt.plot(rt[idx], label=idx[0:3])
    
    plt.legend(shadow=True)

    #plt.legend(handles=plots)
    #for key in rt.keys():
    
    plt.ylabel('rt')
    plt.savefig(filename+str(".png"))
        
        
def plot(filename,arrays,labels,axes,verticals = False):

    x = []
    y = []
    j = 0
    for array in arrays:
        x.append([])
        y.append([])
        i = 0
        for elem in array:
            y[j].append(elem)
            x[j].append(i)
            i+= 1
        j += 1
          
            
    plt.figure(figsize=(20,10))
    plt.clf()
    plt.axis(axes)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    for index, xel in enumerate(x):
        if len(xel) > 0:
            plt.plot(xel, y[index], label=labels[index])
            z = np.polyfit(xel, y[index], 4)
            p = np.poly1d(z)
            plt.plot(xel,p(xel), '--')
    if verticals:
        plt.axvline(64)
        plt.axvline(128)
        plt.axvline(192)
    
    plt.legend(shadow=True)

    #plt.legend(handles=plots)
    #for key in rt.keys():
    
    plt.ylabel('rt')
    plt.savefig(filename+str(".png"))
    

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="file containing the raw experiment data", metavar="FILE", default="merged.csv")
    parser.add_option("-o", "--output", dest="output", help="name of the file to store the calculated data in", metavar="OUT", default="results.csv")
    parser.add_option("--acc-err", dest="error", help="acceptable error rate", metavar="ERR", default=0.1)
    parser.add_option("--acc-std", dest="std", help="acceptable standard deviation from group mean", metavar="STD", default=2.5)
#    parser.add_option("--exclude", dest="exclude", help="exclude given ids from analysis", metavar="EXCL", action="callback", callback=cb_optlists)
    parser.add_option("--exclude",
                  action="append",
                  dest="my_groups")
    (options, args) = parser.parse_args()

    global ALLOWED_ERR
    global ALLOWED_STD
    global EXCLUSION_LIST
    EXCLUSION_LIST = options.my_groups
    ALLOWED_ERR = options.error
    ALLOWED_STD = options.std

    read_file(options.file)
    write_file(options.output)
    #plot_ids("lowest_var", ['2456-d8a7','2c90-57b2','19ac-534e','9d59-4135'])
    #plot_ids("middle", ['31d0-0578','ceaf-1e00','cef2-362a'])
    #plot_ids("highest_var",['06fe-66ef','4439-4896','a764-da29','d93e-4209'])
    
    rt_cond_l_comb = []
    rt_cond_r_comb = []
    x = len(rt) #number of participants
    reject = 0.8 # only if a sample size < #participants*reject use it
    margin = x*reject

    for elem in cond_l_rt:
        if len(elem) > margin:
            rt_cond_l_comb.append(elem.mean())
        
    for elem in cond_r_rt:
        if len(elem) > margin:
            rt_cond_r_comb.append(elem.mean())

    plot("rt_mean_robot_pos", [rt_cond_r_comb, rt_cond_l_comb], ["rt_mean_robotr", "rt_mean_robotl"], [0,256, 380,520], True)
    
    rt_all_compatible_mean = []
    for elem in rt_all_compatible:
        if len(elem) > margin:
            rt_all_compatible_mean.append(elem.mean())    
   
    rt_all_incompatible_mean = []
    for elem in rt_all_incompatible:
        if len(elem) > margin:
            rt_all_incompatible_mean.append(elem.mean())
           
    plot("rt_comptability", [rt_all_compatible_mean, rt_all_incompatible_mean], ["rt_mean_compatible", "rt_mean_incompatible"], [0,128, 380,520])
    
    rt_all_combined_mean = []
    for elem in rt_all_combined:
        if len(elem) > margin:
            rt_all_combined_mean.append(elem.mean())
        
    rt_all_r_combined_mean = []
    for elem in rt_all_r_combined:
        if len(elem) > margin:
            rt_all_r_combined_mean.append(elem.mean())
        
    rt_all_l_combined_mean = []
    for elem in rt_all_l_combined:
        if len(elem) > margin:
            rt_all_l_combined_mean.append(elem.mean())
    
    plot("rt_mean", [rt_all_combined_mean], ["rt_mean"],[0,256, 380,520], True)
    plot("rt_mean_lr", [rt_all_l_combined_mean, rt_all_r_combined_mean], ["rt_mean_l", "rt_mean_r"], [0,128, 380,520])    


if __name__ == '__main__':
    main()

