from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.conf import settings
from django.utils import timezone
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
import traceback
import requests

# Create your views here.
@login_required
@csrf_exempt
def index(request):
	return render(request, 'web/index.html')

@login_required
@csrf_exempt
def check_god_mode_inventory(request):
	data = models.transaction_table.objects.values()
	print data
	return render(request, 'web/index.html')

@login_required
@csrf_exempt
def loan_inventory(request):
	c = {}
	c['message'] = "To be done in Future."
	return render(request, 'web/message.html', c)

@login_required
@csrf_exempt
def buy_position(request):
	c = {}
	state = request.POST.get('state')
	if state is not None:
		district = request.POST.get('district')
		if district is not None:
			market = request.POST.get('market')
			if market is not None:
				commodity = request.POST.get('commodity')
				if commodity is not None:
					variety = request.POST.get('variety')
					if variety is not None:
						current_price_data = models.current_price_table.objects.filter(state=state, district=district, commodity=commodity, variety=variety).values()
					else:
						current_price_data = models.current_price_table.objects.filter(state=state, district=district, commodity=commodity).values()
				else:
					current_price_data = models.current_price_table.objects.filter(state=state, district=district, market=market).values()
			else:
				current_price_data = models.current_price_table.objects.filter(state=state, district=district).values()
		else:
			current_price_data = models.current_price_table.objects.filter(state=state).values()
	else:
		print 'No value passed.'
	#price = request.POST.get('price')
	for data_iter in current_price_datas:
		#{'commodity': u'Groundnut', 'district': u'Anantapur', 'variety': u'Local', 'state': u'Andhra Pradesh', 'min_price': u'4200', 'modal_price': u'4400', 'max_price': u'4600', 'market': u'Anantapur'}
		pass
	return render(request, 'web/buy_position.html', c)

@login_required
@csrf_exempt
def handle_buy_position(request):
	c = {}

	User = request.user.id
	print current_price_datas
	quantity = request.POST.get('quantity')
	crop_type = request.POST.get('crop_type')
	duration = request.POST.get('duration')
	location = request.POST.get('location')
	premium_expected = request.POST.get('premium_expected')
	amount_owned = request.POST.get('amount_owned')
	payment_status = request.POST.get('payment_status')

	return render(request, 'web/buy_position.html')

@login_required
@csrf_exempt
def check_user_inventory(request):
	data = models.transaction_table.objects.filter(User=request.user.id).values()
	print data
	return render(request, 'web/index.html')

@csrf_exempt
def fetch_current_price(request):
	http_response_json = {}
	http_response_json['status'] = False
	http_response_json['message'] = ''
	try:
		url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?format=json&api-key='+str(settings.GOV_API_KEY)+'&limit=5000'
		status_request = requests.get(url)
		final_list = {}
		count = 0

		if status_request and status_request.status_code == requests.codes.ok:
			if status_request != "":
				status_request = status_request.json()
				for record in status_request['records']:
					str_count = str(count)
					final_list[str_count] = {}
					for entry in record:
						final_list[str_count][entry] = record[entry]
					state = final_list[str_count]['state']
					district = final_list[str_count]['district']
					market = final_list[str_count]['market']
					commodity = final_list[str_count]['commodity']
					variety = final_list[str_count]['variety']
					min_price = final_list[str_count]['min_price']
					max_price = final_list[str_count]['max_price']
					modal_price = final_list[str_count]['modal_price']
					arrival_date = final_list[str_count]['arrival_date']
					updated_at = str(timezone.now())
					
					final_list[str_count]['composite_cp_id'] = (state+'_'+district+'_'+market+'_'+commodity+'_'+variety).lower()

					(page_data_save, page_data_save_status)= models.current_price_table.objects.update_or_create(composite_cp_id=str(final_list[str_count]['composite_cp_id']), defaults={'commodity': commodity,'variety': variety,'state': state,'district': district,'market': market,'min_price': min_price,'max_price': max_price,'modal_price': modal_price,'arrival_date': arrival_date,'updated_at': updated_at})
					#Add page_data_save_status to a log file
					print page_data_save_status
					count += 1
			http_response_json['status'] = True
			http_response_json['message'] = final_list
		else:			
			http_response_json['status'] = False
			http_response_json['message'] = "Response is empty OR status code is not ok."
	except Exception as err:
		print traceback.print_exc()
		print err
		http_response_json['status'] = False
		http_response_json['message'] = "Exception occured: %s"%(err)
	finally:
		return HttpResponse(json.dumps(http_response_json), content_type='application/json')