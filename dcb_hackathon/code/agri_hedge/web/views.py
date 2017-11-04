from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
import json
import models
import os
import sys
import traceback
import json
import time
import string
import datetime

# Create your views here.
@login_required
@csrf_exempt
def index(request):
    return render(request, 'web/index.html')
