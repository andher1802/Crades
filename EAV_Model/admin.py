from django.contrib import admin
from EAV_Model.models import *

admin.site.register(Study)
admin.site.register(Stage)
admin.site.register(Patient)
admin.site.register(Cases)

admin.site.register(Health_Center)


admin.site.register(Questions)
admin.site.register(Question_Groups)
admin.site.register(Choices)

admin.site.register(Event_Header)

admin.site.register(EAV)