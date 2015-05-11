from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import *
import logging


def general_templates(request, page):	
	return render_to_response(page,locals())
