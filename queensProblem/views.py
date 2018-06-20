# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render

from random import randint, uniform,random

from datetime import datetime, date, time, timedelta
import random
import numpy as np
import json

def index(request):
    return render(request, 'queensProblem/index.html')

def QueensSimulation(request):
    
    n = int(request.GET.get('n_queens', None))
    r = int(request.GET.get('n_challengers', None))
    arrival_rate = int(request.GET.get('arrival_rate', None))
    matrixResult = []

    counter_r = 1

    while counter_r <= r:
        
        result_challenger = {}
        
        algorithm = SelectAlgorithm()
        result_challenger['algorithm_type'] = algorithm

        if algorithm == "D":
            solucion = []
            
            global td              #Tiempo deterministico
            global solutionDeterministic
            td = 0
            solutionDeterministic = []

            for i in range(n):
                solucion.append(0)
            etapa = 0

            resultDeterministic = DeterministicQueens(solucion, etapa, n)
            result_challenger['solution'] = solutionDeterministic
            result_challenger['time'] = td
            result_challenger['success'] = True
            
        
        else:
            
            successNonDeterministic = False
            tnd = 0                #Tiempo algoritmo no deterministico

            while not successNonDeterministic:
                tnd = tnd +1
                solution2 = []
                for i in range(n):
                    solution2.append(0)
                phase2 = 0
                resultNonDeterministic = NonDeterministicQueens(solution2, phase2, n)
                successNonDeterministic = resultNonDeterministic['success']
            result_challenger.update(resultNonDeterministic)
            result_challenger['time'] = tnd
            print tnd

        print "Contador de retadores >> "
        print counter_r

        

        counter_r = counter_r + 1

        matrixResult.append(result_challenger)

    print "Matriz de resultados >> "
    print matrixResult

    json_matrix = json.dumps(matrixResult)

    return HttpResponse(json_matrix, content_type="application/json")

#  Método que calcula la posición de n-reinas de forma determinística
#  Método que calcula la posición de n-reinas de forma determinística
def DeterministicQueens(solution, phase, n):

    global td
    global solutionDeterministic

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
                    print "Solución Determinista >> "
                    print solution
                    solutionDeterministic = solution
                    success = True
            if (solution[phase]==n or success==True):
                break

    return success

# Método que calcula la posición de n-reinas de forma no determinística
# utilizando un algoritmo Las Vegas Tipo 2
def NonDeterministicQueens(solution, phase, n):

    columns = []
    solution = []
    result = {}
    result['success'] = True
    phase = 0

    for i in range(n):
        columns.append(i+1)
        solution.append(0)

    for i in range(n):
        index = random.randint(0, len(columns)-1)
        solution[phase] = columns[index]
        columns.pop(index)

        if not isValid(solution, phase):
            result['success'] = False
            break
            
        #print index, columns, solution, isValid(solution, phase), phase
        phase = phase + 1
    
    print "Solución no Determinista >> "
    print solution

    result['solution'] = solution

    return result


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

def SelectAlgorithm():
    prob = np.random.rand()
    print prob
    if prob <= 0.5:
        return 'D'
    else:
        return 'P'


