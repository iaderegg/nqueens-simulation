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
import math

def index(request):
    return render(request, 'queensProblem/index.html')

def QueensSimulation(request):

    n = int(request.GET.get('n_queens', None))
    r = int(request.GET.get('n_challengers', None))
    arrival_rate = int(request.GET.get('arrival_rate', None))
    desvest_arrival_rate = int(request.GET.get('desvest_arrival_rate', None))
    matrixResult = []
    master_status = False  # Refleja si el maestro está ocupado o no

    result_simulation = {}

    counter_r = 0

    while counter_r < r:
        
        counter_r = counter_r + 1
        
        result_challenger = {}

        result_challenger['challenger'] = counter_r

        if counter_r == 1:
            result_challenger['arrival_time'] = 0
            result_challenger['inter_arrival_time'] = 0
        else:
            arrival_random = math.floor(np.random.normal(arrival_rate, desvest_arrival_rate))
            result_challenger['inter_arrival_time'] = arrival_random
            result_challenger['arrival_time'] = int(matrixResult[counter_r-2]['arrival_time']) + arrival_random
        
        algorithm = SelectAlgorithm()
        result_challenger['algorithm_type'] = algorithm

        # Si se escoge un algoritmo deterministico
        if algorithm == "D":
            solucion = []
            
            global td              #Tiempo algoritmo deterministico
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

            if counter_r == 1:
                result_challenger['exit_time'] = td
                result_challenger['start_attention'] = 0
                result_challenger['waiting_time'] = 0
                result_challenger['max_queue'] = 0

            else:
                start_attention = int(matrixResult[counter_r-2]['exit_time']) + 1

                if start_attention < result_challenger['arrival_time']:
                    result_challenger['start_attention'] = result_challenger['arrival_time']
                else:
                    result_challenger['start_attention'] = int(matrixResult[counter_r-2]['exit_time']) + 1

                result_challenger['exit_time'] = int(result_challenger['start_attention']) + td
                result_challenger['waiting_time'] = int(result_challenger['start_attention']) - int(result_challenger['arrival_time'])

        # Si se escoge un algoritmo probabilistico
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

            if counter_r == 1:
                result_challenger['exit_time'] = tnd
                result_challenger['start_attention'] = 0
                result_challenger['waiting_time'] = 0
                result_challenger['max_queue'] = 0

            else:
                start_attention = int(matrixResult[counter_r-2]['exit_time']) + 1

                if start_attention < result_challenger['arrival_time']:
                    result_challenger['start_attention'] = result_challenger['arrival_time']
                else:
                    result_challenger['start_attention'] = int(matrixResult[counter_r-2]['exit_time']) + 1

                result_challenger['exit_time'] = int(result_challenger['start_attention']) + tnd
                result_challenger['waiting_time'] = int(result_challenger['start_attention']) - int(result_challenger['arrival_time'])

            print tnd

        matrixResult.append(result_challenger)

        #print "Contador de retadores >> "
        #print counter_r

    #print "Matriz de resultados >> "
    #print matrixResult

    performance_rates = calculate_performance_simulation(matrixResult, r)

    result_simulation['performance_rates'] = performance_rates
    result_simulation['matrix_result'] = matrixResult

    json_result = json.dumps(result_simulation)

    return HttpResponse(json_result, content_type="application/json")

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

def calculate_performance_simulation(matrix_result, r):

    performance = {}
    sum_time_queue = 0
    sum_time_master = 0

    for i in range(len(matrix_result)):

        sum_time_master = sum_time_master + matrix_result[i]['time']

        if i != 0:
            sum_time_queue = sum_time_queue + matrix_result[i]['waiting_time']

    av_time_queue = sum_time_queue/r
    av_master = sum_time_master/r
    
    performance['av_time_queue'] = av_time_queue
    performance['av_master'] = av_master

    return performance
