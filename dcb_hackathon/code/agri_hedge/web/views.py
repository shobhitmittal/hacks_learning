from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

# Create your views here.
def fetch_current_price():
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
					final_list[str(count)] = {}
					for entry in record:
						final_list[str(count)][entry] = record[entry]
					state = final_list[str(count)]['state']
					district = final_list[str(count)]['district']
					market = final_list[str(count)]['market']
					commodity = final_list[str(count)]['commodity']
					variety = final_list[str(count)]['variety']
					min_price = final_list[str(count)]['min_price']
					max_price = final_list[str(count)]['max_price']
					modal_price = final_list[str(count)]['modal_price']
					arrival_date = final_list[str(count)]['arrival_date']
					updated_at = timezone.now
					
					final_list[str(count)]['composite_cp_id'] = state.lower()+'_'+district.lower()+'_'+market.lower()+'_'+commodity.lower()+'_'+variety.lower()

					(page_data_save, page_data_save_status)= models.current_price_table.objects.update_or_create(composite_cp_id=str(final_list[str(count)]['composite_cp_id']), defaults={'commodity': commodity,'variety': variety,'state': state,'district': district,'market': market,'min_price': min_price,'max_price': max_price,'modal_price': modal_price,'arrival_date': arrival_date,'updated_at': updated_at})
					count += 1
			http_response_json['status'] = True
			http_response_json['message'] = final_list
		else:			
			http_response_json['status'] = False
			http_response_json['message'] = "Response is empty OR status code is not ok."
	except Exception as err:
		http_response_json['status'] = False
		http_response_json['message'] = "Exception occured: %s"%(err)
	finally:
		return HttpResponse(http_response_json, content_type='application/json')

		(page_data_save, page_data_save_status)= models.Page.objects.update_or_create(page_id=str(page_data['id']), defaults={'page_name': page_data['name'],'likes': page_data['likes'],'talking_about_count': page_data['talking_about_count']})