# Create your views here.
from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login as auth_login
from datetime import datetime

import logging
import inspect

def login_user(request):
    state = "Please log in below..."
    errors = []
    username = password = ''
    c = Context({'state':state})

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect("/eav/patient")
            else:
                errors.append("That account is disabled") 
        else:
            errors.append("Invalid answer or password")
        
        c = Context({'state':state, 'errors':errors[len(errors)-1]})
        return render(request, './auth.html', c)
    else:
        return render(request, './auth.html', c)

from EAV_Model.models import *
from EAV_Model.forms import *
from django.contrib.auth.models import User

@login_required
def Patient_View(request):
    if request.method == 'POST': # If the form has been submitted...
        Pat_form = Patient_form(request.POST) # A form bound to the POST data
        Cas_form = Cases_form(request.POST) 

        if Pat_form.is_valid() and Cas_form.is_valid():
            
            patientUserOrder = Patient.objects.filter(userOwner = request.user)
            patientOrder = len(patientUserOrder)+1
            
            patInstance = Patient(patientUserOrder = int(patientOrder), userOwner = request.user)
            patForm = Patient_form(request.POST, instance=patInstance)
            patForm.save()

            patientObject = Patient.objects.get(patientCode = request.POST['patientCode'])
            healthCenter = Health_Center.objects.get(idHealthCenter = request.POST['idCaseCenter'])
            
            caseInstance = Cases(idCasePatient = patientObject, idCaseCenter = healthCenter)
            caseForm =  Cases_form(request.POST, instance=caseInstance)
            caseForm.save()

            casesObject = Cases.objects.get(idCasePatient = patientObject.idPatient)

            eventInstance = Event_Header(patientId = patientObject, injuryId = casesObject, dateCollected = datetime.datetime.now(), verified = False, completed = False, problems = 'temporal')
            eventInstance.save()

            firstStudy = request.POST['studyId']
            studyName = Study.objects.get(idStudy = int(firstStudy)).studyName
            firstStage = Stage.objects.filter(studyId=int(firstStudy)).get(order=1)
            return redirect("/eav/"+studyName+'/main/')

            Cas_form = Cases_form()
            Pat_form = Patient_form()

        c = Context({'Pat_form':Pat_form, 'Cas_form':Cas_form})
    
    else:
        Pat_form = Patient_form()
        Cas_form = Cases_form()

        Study_List = []

        for element in Study.objects.all():
            studyNameStr = str(element).split(" ")[0]
            Study_List.append(studyNameStr)

        c = Context({'Pat_form':Pat_form, 'Cas_form':Cas_form, 'Study':Study_List})

    logging.debug('Context'+str(c))
    return render(request, './main.html',c)

@login_required
def Main_View(request):
    path = request.path
    elements = path.split("/")
    studyNameChar = elements[2]

    studyName = Study.objects.get(studyName = studyNameChar)
    stages = Stage.objects.filter(studyId=int(studyName.idStudy)).order_by('order')

    listStages = []
    for element in stages:
        listStages.append(element.stageType)

    c = Context({'Study':studyNameChar,'Stages':listStages})
    return render(request, './entry_point.html',c)

from Utils import test_textload
import sys
sys.path.append("../")

from django.utils import encoding
import re

@login_required
def Form_View(request):
    logging.debug('Hello')
    pathComplete = str(request.path)
    elements = pathComplete.split("/")
    studyName = elements[2]
    stageName = elements[3]
    currentStudy = Study.objects.get(studyName = studyName)
    currentStage = Stage.objects.get(stageType = stageName, studyId = currentStudy)
    currentPosition = currentStage.order
    frame = currentStage.helpContent
    patientsList = Patient.objects.filter(studyId__idStudy = currentStudy.idStudy, userOwner = request.user)
    logging.info("BROWSER: "+request.META['HTTP_USER_AGENT'])

    if request.method == 'POST':
        ANSWER = request.POST
        form = DynForm(request.path, request.user, ANSWER)

        if form.is_valid():

            currentPatient = str(ANSWER['Paciente']).split(" ")
            patientId = currentPatient[2]

            patientName = Patient.objects.get(patientCode = patientId)
            entity = Event_Header.objects.get(patientId = patientName.idPatient)

            for questElement in ANSWER.keys():
                currentQuestion = str(questElement).split(" ")
                logging.info(currentQuestion)
                Element = currentQuestion[0]
                logging.info(Element)

                if Element=='csrfmiddlewaretoken' or Element=='Paciente':
                    continue

                if ANSWER[questElement] == "":
                    continue

                logging.info(Element)

                Quest = Questions.objects.get(questionsName = Element)
                Registry = EAV(timeStamp = datetime.datetime.now(), headerId = entity, phaseId = currentStage, questionId = Quest)                
                if Quest.questionsType=='Int':
                    Registry.valuesInteger = ANSWER[questElement]
                elif Quest.questionsType=='Char':
                    Registry.valuesChar = ANSWER[questElement]
                elif Quest.questionsType=='Real':
                    Registry.valuesFloat = ANSWER[questElement]
                elif Quest.questionsType=='Date':
                    Registry.valuesDate = ANSWER[questElement]
                elif Quest.questionsType=='Time':
                    Registry.valuesTime = ANSWER[questElement]
                elif Quest.questionsType=='Bool':
                    Registry.valuesBool = ANSWER[questElement]
                elif Quest.questionsType=='Enum':
                    Registry.valuesEnum = ANSWER[questElement]
                Registry.save()

            form = DynForm(request.path, request.user)
            c = Context({'Q_forms':form, 'frame':frame, 'patientsList':patientsList})
            return redirect("/eav/"+str(studyName)+'/main/')

        else: 
            c = Context({'Q_forms':form,'frame':frame, 'patientsList':patientsList})
    else:
        form = DynForm(request.path , request.user)
        
        listHeaders = []
        listChilds = []
        listRel = []
        listRelTypes = []

        for questionGroups in Question_Groups.objects.filter(groupStage__idStage = currentStage.idStage).order_by('order'):
            i = 0
            listTemp = []
            
            # logging.info(inspect.getmembers(questionGroups.idQuestions, predicate=inspect.ismethod))
            # logging.info(len(questionGroups.idQuestions.values()))
            if(len(questionGroups.idQuestions.values())>1):
                for question in questionGroups.idQuestions.all():
                    listTemp.append('id_%s' % (str(question.questionsName)))
                listHeaders.append(listTemp[questionGroups.groupHeader-1])
                listRel.append(questionGroups.relation)
                listRelTypes.append(questionGroups.inverseRelated)
                listTemp.pop(questionGroups.groupHeader-1)
                listChilds.append(list(listTemp))

            dictRelation = {}
            for i in range(0, len(listHeaders)):
                dictRelation[listHeaders[i]] = (listRel[i], listChilds[i], listRelTypes[i])

        script = test_textload.scriptLoader(dictRelation)

        c = Context({'Q_forms':form, 'Study':studyName, 'Stage':currentStage, 'Script':script, 'frame':frame, 'patientsList':patientsList})

    return render(request, './generic_form.html',c)