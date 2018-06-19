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

#  Método que calcula la posición de n-reinas de forma determinística
def DeterministicQueens(solution, phase, n, t):
    
    if phase>=n:
        return False

    success = False

    while True:
            if (solution[phase] < n):
                solution[phase] = solution[phase] + 1

            if (isValid(solution, phase)):

                if phase != n-1:
                    success = DeterministicQueens(solution, phase+1, n, t+1)
                    if success==False:
                        solution[phase + 1] = 0

                else:
                    print solution
                    print t
                    success = True
            if (solution[phase]==n or success==True):
                break
    return success

# Método que calcula la posición de n-reinas de forma no determinística
# utilizando un algoritmo Las Vegas Tipo 2
def NonDeterministicQueens(solution, phase, n, t):

    if phase>=n:
        return False

    t = t + 1
    success = False   

    while True:
            
            if (solution[phase] < n):
                solution[phase] = random.randint(1, n)
            print "Solucion y fase"
            print solution, phase
            print isValid(solution, phase)
            if (isValid(solution, phase)):

                if phase != n-1:
                    success = NonDeterministicQueens(solution, phase+1, n, t)
                    print solution, phase

                else:
                    print solution
                    success = True
            else:
                return False
                break

            if (solution[phase]==n or success==True):
                break
      
    return success


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


print "PROBLEMA DE LAS N - REINAS"
print "#"*26
print "\n"
print "Introduce el numero de reinas:\n"

n = input()
solucion = []
for i in range(n):
	solucion.append(0)
etapa = 0
t = 0
print DeterministicQueens(solucion, etapa, n, t)

solution2 = []
for i in range(n):
	solution2.append(0)
phase2 = 0
print NonDeterministicQueens(solution2, phase2, n, t)