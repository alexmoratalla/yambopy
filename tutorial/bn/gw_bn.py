#
# Author: Henrique Pereira Coutada Miranda
# Run a GW calculation using Yambo
#
from __future__ import print_function
from yambopy import *
from qepy import *
from schedulerpy import * #USE SCHEDULERPY INSTEAD OF OS

yambo =  'yambo'

if not os.path.isdir('database'):
    os.mkdir('database')

#check if the nscf cycle is present
if os.path.isdir('nscf/bn.save'):
    print('nscf calculation found!')
else:
    print('nscf calculation not found!')
    exit()

#check if the SAVE folder is present
if not os.path.isdir('database/SAVE'):
    print('preparing yambo database')
    os.system('cd nscf/bn.save; p2y')
    os.system('cd nscf/bn.save; yambo')
    os.system('mv nscf/bn.save/SAVE database')

if not os.path.isdir('gw'):
    os.mkdir('gw')
    os.system('cp -r database/SAVE gw')

#create the yambo input file
y = YamboIn.from_runlevel('%s -d -g n -V all'%yambo,folder='gw')
QPKrange,_ = y['QPkrange']
y['QPkrange'] = [QPKrange[:2]+[4,5],'']
y['FFTGvecs'] = [30,'Ry']
y['NGsBlkXd'] = [1,'Ry']
y['BndsRnXd'] = [[1,30],'']
y.write('gw/yambo_run.in')

print('running yambo')
os.system('cd gw; %s -F yambo_run.in -J yambo'%yambo)
