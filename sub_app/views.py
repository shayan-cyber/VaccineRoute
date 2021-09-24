from django.shortcuts import render
import requests
import json
import datetime




# Create your views here.
def home(request):
    # pin = 781034
    # date = '23-09-2021'
    # COWIN_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}"
    # print(COWIN_URL)
    # resp = requests.get(COWIN_URL)
    # # print(resp.json())
    # # print(json.loads(resp))
    # resp_json = resp.json()
    # for i in resp_json['sessions']:
    #     print(i)
    #     print('\n')
    #     print(i['lat'])


    context = {
        # 'resp':resp.json(),
    }

    return render(request, 'index.html',context )
def select_location(request):
    
    if request.method == 'POST':
        pos = request.POST.get('pos', '')
        pin = request.POST.get('pin', '')
        type_ = request.POST.get('type', '')
        print(type_)
        
        #converting to tuple
        pos = eval(pos) 
        #roundoff
        lat = str(round(pos[0], 2))
        longi = str(round(pos[1], 2))

        print(lat)
        print(longi)

        #API Fetch
        if type_ == 'map':

            lat_long_url = f'https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong?lat={lat}&long={longi}'
            headers = {
            'accept': 'application/json',
            'Accept-Language': 'hi_IN'
            }
            print(lat_long_url)
            resp = requests.get(lat_long_url ,headers=headers)
            
            resp_json = resp.json()
        
            # for i in resp_json['sessions']:
            #     print(i)
            #     print('\n')
            #     print(i['lat'])
            centers = resp_json['centers']
            # print(centers)
            centers_list = {}
            for i in centers:
                # print(i)
                # print('\n')
                centers_list[str(i['name'])] = {
                    'center_id':i['center_id'],
                    'pincode':i['pincode'],
                    'lat':i['lat'],
                    'lng':i['long'],
                }
                # centers_list.append(i)
            
            # print("list:")
            # print("\n")
            # print(centers_list)
            context ={
                'centers_list':centers_list,
                'centers':resp_json,
                'lat':lat,
                'longi':longi

            }
        elif type_ == 'pin':
            print(pin)
            today= datetime.date.today()
            d1 = today.strftime("%d-%m-%Y")
            print(d1)
            # date = '23-09-2021'
            
            COWIN_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={d1}"
            print(COWIN_URL)
            resp = requests.get(COWIN_URL)
            # print(resp.json())
            # print(json.loads(resp))
            resp_json = resp.json()
            centers_list = {}
            print(resp_json)
            for i in resp_json['sessions']:
                # print("center")
                # print("\n")
                # print(i)
                # print('\n')
                centers_list[str(i['name'])] = {
                    'center_id':i['center_id'],
                    'pincode':i['pincode'],
                    'lat':i['lat'],
                    'lng':i['long'],
                }
                # print(i['lat'])
            print(centers_list)
            context ={
                'centers_list':centers_list,
                'centers':resp_json,
                'lat':lat,
                'longi':longi,
                'pin':True,

            }





    return render(request, 'select_location.html', context)

def get_route(request,center_id,pincode, lat, longi, cur_lat, cur_longi):
    print(center_id)
    print(pincode)
    print(lat)
    print(longi)
    print(cur_lat)
    print(cur_longi)

    today= datetime.date.today()
    d1 = today.strftime("%d-%m-%Y")
    print(d1)
    # date = '23-09-2021'
    
    COWIN_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={d1}"
    print(COWIN_URL)
    resp = requests.get(COWIN_URL)
   
    resp_json = resp.json()
    details = {}
   
    for i in resp_json['sessions']:
        print(i['center_id'])
        
        if str(i['center_id']) == str(center_id):

            print("yes")
            details['Name']= i['name']
            details['Available capacity dose one'] = i['available_capacity_dose1']
            details['Available capacity dose two'] = i['available_capacity_dose2']
            details['Vaccine'] = i['vaccine']


    # for i in centers:
    #     if i['center_id'] == center_id:
    #         pass
    print(details)
    context ={
        'start_lat':lat,
        'start_long':longi,
        'end_lat':cur_lat,
        'end_long':cur_longi,
        'details':details,
    }


    
    return render(request, 'get_route.html', context)