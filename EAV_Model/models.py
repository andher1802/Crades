from django.db import models 
from django.contrib import admin
import datetime

# Create your models here.
class Study(models.Model):
    idStudy = models.AutoField(primary_key=True)
    studyName = models.CharField(max_length = 150, unique=True)
    startingDate = models.DateField(default=datetime.date.today)
    
    def __str__(self):
    	return '%s %s' % (self.studyName, self.startingDate)
	class Admin:
		pass

class Stage(models.Model):
	idStage = models.AutoField(primary_key=True)
	order = models.IntegerField()
	studyId = models.ForeignKey(Study, db_column="idStudy")
	stageType = models.CharField(max_length = 150)
	helpContent = models.URLField()
	class Meta:
		unique_together=(("studyId", "stageType"),("studyId", "order"))

	def __str__(self):
		return '%s %s %s' % (self.order, self.stageType, self.studyId)
	class Admin:
		pass

GENDER_CHOICES = (('M', 'Masculino'),('F', 'Femenino'),)
ORIGIN_CHOICES = (('Rural', 'Rural'),('Urbano', 'Urbano'),)

class Patient(models.Model):
	idPatient = models.AutoField(primary_key=True)
	patientUserOrder = models.IntegerField()
	studyId = models.ForeignKey(Study, db_column="idStage")
	patientCode = models.CharField((u"Id. del Paciente"), max_length = 150, unique=True)
	# originCountry = models.CharField((u"Pais de Origen"), max_length = 150)
	# originCity = models.CharField((u"Ciudad de Origen"), max_length = 150)
	# originZone = models.CharField((u"Zona de Origen"), max_length = 150, choices=ORIGIN_CHOICES, default='Rural')
	age = models.IntegerField((u"Edad"), blank=True)
	gender = models.CharField((u"Genero"), max_length = 1, choices=GENDER_CHOICES, default='M')
	userOwner = models.CharField(max_length = 150)

	def __str__(self):
		return '%s %s %s %s' % (self.patientUserOrder, self.patientCode, self.gender, self.userOwner)
	class Admin:
		pass

HC_CLASS_CHOICES = (('Rural', 'Rural'),('Urban', 'Urban'),('Intermediate', 'Intermediate'),('Advanced', 'Advanced'),)
HC_CITIES = (('Neiva', 'Neiva'),('Pereira', 'Pereira'),('Valledupar', 'Valledupar'),('Kennedy', 'Kennedy'),('Cali', 'Cali'),('Buenos_Aires', 'Buenos_Aires'),('Pasto', 'Pasto'),)

class Health_Center(models.Model):
	idHealthCenter = models.AutoField(primary_key=True)
	studyId = models.ManyToManyField(Study)
	name = models.CharField((u"Nombre de la Institucion"), max_length = 150)
	# classification = models.CharField((u"Clasificacion de la Institucion"), max_length = 150, choices=HC_CLASS_CHOICES, default='Intermediate')
	
	def __str__(self):
		return '%s %s' % (self.idHealthCenter, self.name)
	class Admin:
		pass

class Cases(models.Model):
	idCase = models.AutoField(primary_key=True)
	idCasePatient = models.ForeignKey(Patient, db_column="idPatient")
	idCaseCenter = models.ForeignKey(Health_Center, db_column="idHealthCenter")
	caseDate = models.DateField(default=datetime.date.today)
		
	def __str__(self):
		return '%s %s' % (self.idCasePatient, self.idCaseCenter)
	class Admin:
		pass

Type = (('Char', 'Char'), ('Int', 'Int'), ('Real', 'Real'),
        ('Date', 'Date'), ('Time', 'Time'), ('Bool', 'Bool'),
        ('Img', 'Img'), ('Enum', 'Enum'),)

class Questions(models.Model):
	questionsId = models.AutoField(primary_key=True)
	questionsLabel = models.TextField()
	questionsName = models.CharField(max_length = 150)
	questionsType = models.CharField(max_length = 150, choices=Type, default='Int')
	questionsDescription = models.TextField()
	questionHelp = models.TextField()
	questionMin = models.IntegerField(blank=True, null=True)
	questionMax = models.IntegerField(blank=True, null=True)
	comments = models.TextField()

	def __str__(self):
		return '%s' % (self.questionsName)
	class Admin:
		pass

class Choices(models.Model):
	choiceId = models.AutoField(primary_key=True)
	questionId = models.ManyToManyField(Questions)
	choiceName = models.CharField(max_length = 150, unique=True)
	
	def __str__(self):
		return '%s' % (self.choiceName)
	class Admin:
		pass

class Question_Groups(models.Model):
	questionsGroupId = models.AutoField(primary_key=True)
	order = models.IntegerField()
	questionGroupName = models.CharField(max_length = 150)
	idQuestions = models.ManyToManyField(Questions, null=True)
	groupStage = models.ForeignKey(Stage, db_column="idStage")
	groupHeader = models.IntegerField()
	relation = models.CharField(max_length = 150)
	inverseRelated = models.BooleanField()

	def __str__(self):
		return '%s %s' % (self.questionsGroupId, self.questionGroupName)
	class Admin:
		pass

class Event_Header(models.Model):
	headerId = models.AutoField(primary_key=True)
	patientId = models.ForeignKey(Patient, db_column="idPatient", editable=True, unique=True)
	injuryId =  models.ForeignKey(Cases, db_column="idCase", editable=True)
	dateCollected = models.DateTimeField()
	verified = models.BooleanField()
	completed = models.BooleanField()
	problems = models.TextField()
	
	def __str__(self):
		return '%s %s %s' % (self.patientId, self.injuryId, self.dateCollected)
	class Admin:
		pass

class EAV(models.Model):
	timeStamp = models.DateTimeField()
	headerId = models.ForeignKey(Event_Header, db_column="headerId")
	phaseId = models.ForeignKey(Stage, db_column="idStage")
	questionId =  models.ForeignKey(Questions, db_column="questionsId")
	valuesInteger = models.IntegerField(null=True, blank=True)
	valuesChar = models.CharField(max_length = 150, null=True, blank=True)
	valuesFloat = models.FloatField(null=True, blank=True)
	valuesDate = models.DateField(null=True, blank=True)
	valuesTime = models.TimeField(null=True, blank=True)
	valuesBool = models.NullBooleanField(null=True, blank=True)
	valuesEnum = models.CharField(max_length = 150, null=True, blank=True)
	
	def __str__(self):
		return '%s %s - %s %s %s %s %s %s %s' % (self.headerId, self.questionId, self.valuesInteger, self.valuesChar, self.valuesFloat, self.valuesDate, self.valuesTime, self.valuesBool, self.valuesEnum)
	class Admin:
		pass