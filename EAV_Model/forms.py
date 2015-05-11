from django.forms import ModelForm, Form 
from django.forms.fields import CharField, IntegerField, FloatField, BooleanField, FileField, ChoiceField, DateField, TimeField, NullBooleanField

from EAV_Model.models import *

import floppyforms as forms

class Patient_form(ModelForm):
	class Meta:
		model = Patient
		fields = ('studyId', 'patientCode', 'age', 'gender')
		widgets = {
		'age': forms.NumberInput(attrs = {'max': 200, 'min': 0, 'step': 1}),
		'studyId':forms.Select
		}

	def __init__(self, *args, **kwargs):
		super(Patient_form, self).__init__(*args, **kwargs)
		self.fields['studyId'].label = "Elija estudio"
		self.fields['studyId'].widget.attrs['class'] = 'form-control'
		self.fields['patientCode'].widget.attrs['class'] = 'form-control'
		self.fields['age'].widget.attrs['class'] = 'form-control'
		self.fields['gender'].widget.attrs['class'] = 'form-control'


class Cases_form(ModelForm):
	class Meta:
		model = Cases
		fields = ('idCaseCenter', 'caseDate')
		widgets = {
		'caseDate': forms.DateInput,
		'idCaseCenter': forms.Select,
		}

	def __init__(self, *args, **kwargs):
		super(Cases_form, self).__init__(*args, **kwargs)
		self.fields['caseDate'].label = "Fecha del evento"
		self.fields['idCaseCenter'].label = "Institucion"
		self.fields['idCaseCenter'].widget.attrs['class'] = 'form-control'
		self.fields['caseDate'].widget.attrs['class'] = 'form-control'

class DynForm(Form):
    def __init__(self, path, user, *args, **kwargs):
        super(DynForm, self).__init__(*args, **kwargs)
        pathComplete = str(path)
        elements = pathComplete.split("/")
    	studyName = elements[2]
    	stageName = elements[3]

        for study in Study.objects.filter(studyName=str(studyName)):
        	tempEntity = []

        	for entity in Patient.objects.filter(studyId__idStudy = study.idStudy, userOwner = user):
        		tempLabel = str(entity).split(" ")
        		patientLabel = tempLabel[0]+". ID: "+tempLabel[1]
        		tempEntity.append((patientLabel,patientLabel))

        	choiceEnt = tuple(tempEntity)
        	self.fields['Paciente'] = ChoiceField(tempEntity, initial=tempEntity[len(tempEntity)-1])
        	self.fields['Paciente'].widget.attrs['class'] = 'form-control'


        	for stage in Stage.objects.filter(studyId=study.idStudy):
        		if stage.stageType == str(stageName):
        			questionList = []
        			for questionGroups in Question_Groups.objects.filter(groupStage__idStage = stage.idStage).order_by('order'):

        				for question in questionGroups.idQuestions.all():
        					questionList.append(question)

        				for question in questionList:
							if question.questionsType == 'Char':
								self.fields['%s' % question] = CharField(max_length=255, required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
							if question.questionsType == 'Int':
								self.fields['%s' % question] = IntegerField(widget=forms.NumberInput(), required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
								self.fields['%s' % question].widget.attrs['min'] = question.questionMin
								self.fields['%s' % question].widget.attrs['max'] = question.questionMax
								self.fields['%s' % question].widget.attrs['step'] = 1
							if question.questionsType == 'Real':
								self.fields['%s' % question] = FloatField(widget=forms.NumberInput(), required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
								self.fields['%s' % question].widget.attrs['min'] = question.questionMin
								self.fields['%s' % question].widget.attrs['max'] = question.questionMax
								self.fields['%s' % question].widget.attrs['step'] = 0.1
							if question.questionsType == 'Date':
								self.fields['%s' % question] = DateField(widget=forms.DateInput(),required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
							if question.questionsType == 'Time':
								self.fields['%s' % question] = TimeField(widget=forms.TimeInput(), required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
							if question.questionsType == 'Bool':
								self.fields['%s' % question] = NullBooleanField(widget=forms.NullBooleanSelect(), required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs.update({'onclick': "toggle_id_%s()" % question,})
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'					
							if question.questionsType == 'Img':
								self.fields['%s' % question] = FileField(required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'
							if question.questionsType == 'Enum':
								choices = Choices.objects.filter(questionId__questionsId = question.questionsId)

								list_of_choices = []
								for choice in choices:
									list_of_choices.append((choice, choice))
								tuple_of_choices = tuple(list_of_choices) 
								self.fields['%s' % question] = ChoiceField(widget=forms.Select(),choices=tuple_of_choices, required=False)
								self.fields['%s' % question].label = str(question.questionsLabel)
								self.fields['%s' % question].help_text = str(question.questionHelp)
								self.fields['%s' % question].widget.attrs.update({'onchange': "toggle_id_%s()" % question,})
								self.fields['%s' % question].widget.attrs['class'] = 'form-control'	
