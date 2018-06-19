# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from random import randint, uniform,random

import sys
from datetime import datetime, date, time, timedelta
import random
sys.setrecursionlimit(100000)

def index(request):
    return HttpResponse("Hello world!!")

def QueensSimulation(n):
    
    solucion = []
    tnd = 0                #Tiempo algoritmo no deterministico
    global td              #Tiempo deterministico
    td = 0
    for i in range(n):
        solucion.append(0)
    etapa = 0
    DeterministicQueens(solucion, etapa, n)
    

    successNonDeterministic = False

    while not successNonDeterministic:
        tnd = tnd +1
        solution2 = []
        for i in range(n):
            solution2.append(0)
        phase2 = 0
        successNonDeterministic = NonDeterministicQueens(solution2, phase2, n)
    print tnd
    

#  Método que calcula la posición de n-reinas de forma determinística
def DeterministicQueens(solution, phase, n):
    
    global td
    if phase>=n:
        return False

    success = False

    while True:
            if (solution[phase] < n):
                solution[phase] = solution[phase] + 1

            if (isValid(solution, phase)):

                if phase != n-1:
                    success = DeterministicQueens(solution, phase+1, n)
                    if success==False:
                        
                        solution[phase + 1] = 0
                        td = td + 1
                        


                else:
                    print solution
                    print td
                    success = True
            if (solution[phase]==n or success==True):
                break
    return success

# Método que calcula la posición de n-reinas de forma no determinística
# utilizando un algoritmo Las Vegas Tipo 2
def NonDeterministicQueens(solution, phase, n):

    columns = []
    solution = []
    phase = 0
    for i in range(n):
        columns.append(i+1)
        solution.append(0)
    
    print columns

    for i in range(n):
        index = random.randint(0, len(columns)-1)
        solution[phase] = columns[index]
        columns.pop(index)

        print index, columns, solution, isValid(solution, phase), phase

        if not isValid(solution, phase):
            return False

        phase = phase + 1
    
    return solution


def isValid(solution,phase):
	# Comprueba si el vector solucion construido hasta la etapa es 
	# prometedor, es decir, si la reina se puede situar en la columna de la etapa
	for i in range(phase):
		if(solution[i] == solution[phase]) or (absVal(solution[i],solution[phase]) == absVal(i,phase)):
			return False

	return True

def absVal(a, b):
	if a > b:
		return a - b
	else:
		return b - a	

QueensSimulation(8)