from django.urls import path

from .views import *
from store import views

urlpatterns = [

    path('get-consignor-ajax/', get_consignor_ajax, name="get_consignor_ajax"),
   
    path('add-company/', add_company, name='add_company'),
    path('update-company/<company_id>', update_company, name='update_company'),
    path('delete-company/<company_id>', delete_company, name='delete_company'),
    path('list-company/', list_company, name='list_company'),

    path('add-office_location/', add_office_location, name='add_office_location'),
    path('update-office_location/<office_location_id>', update_office_location, name='update_office_location'),
    path('delete-office_location/<office_location_id>', delete_office_location, name='delete_office_location'),
    path('list-office_location/', list_office_location, name='list_office_location'),

    path('add-company-consignor/', add_consignor, name='add_consignor'),
    path('add-company-consignor-ajax/', add_consignor_ajax, name='add_consignor_ajax'),
    path('update-company-consignor/<consignor_id>', update_consignor, name='update_consignor'),
    path('delete-company-consignor/<consignor_id>', delete_consignor, name='delete_consignor'),
    path('list-company-consignor/', list_consignor, name='list_consignor'),

    
    path('add-article/', add_article, name='add_article'),
    path('add-article-ajax/', add_article_ajax, name='add_article_ajax'),
    path('update-article/<article_id>', update_article, name='update_article'),
    path('delete-article/<article_id>', delete_article, name='delete_article'),
    path('list-article/', list_article, name='list_article'),

    path('add-truck-details/', add_truck_details, name='add_truck_details'),
    path('add-truck-details-ajax/', add_truck_details_ajax, name='add_truck_details_ajax'),
    path('update-truck-details/<truck_details_id>', update_truck_details, name='update_truck_details'),
    path('delete-truck-details/<truck_details_id>', delete_truck_details, name='delete_truck_details'),
    path('list-truck-details/', list_truck_details, name='list_truck_details'),
    
    path('add-truck-other/', add_truck_owner, name='add_truck_owner'),
    path('add-truck-other-ajax/', add_truck_owner_ajax, name='add_truck_owner_ajax'),
    path('update-truck-other/<truck_owner_id>', update_truck_owner, name='update_truck_owner'),
    path('delete-truck-other/<truck_owner_id>', delete_truck_owner, name='delete_truck_owner'),
    path('list-truck-other/', list_truck_owner, name='list_truck_owner'),
    
    path('add-rate/', add_rate, name='add_rate'),
    path('update-rate/<rate_id>', update_rate, name='update_rate'),
    # path('delete-truck-other/<rate_id>', delete_rate, name='delete_rate'),
    path('list-rate/', list_rate, name='list_rate'),
    
    path('add-onaccount/', add_onaccount, name='add_onaccount'),
    path('add-onaccount-ajax/', add_onaccount_ajax, name='add_onaccount_ajax'),
    path('update-onaccount/<onaccount_id>', update_onaccount, name='update_onaccount'),
    path('delete-onaccount/<onaccount_id>', delete_onaccount, name='delete_onaccount'),
    path('list-onaccount/', list_onaccount, name='list_onaccount'),
    
    path('add-driver/', add_driver, name='add_driver'),
    path('update-driver/<driver_id>', update_driver, name='update_driver'),
    path('delete-driver/<driver_id>', delete_driver, name='delete_driver'),
    path('list-driver/', list_driver, name='list_driver'),
    
    path('add-petrol_pump/', add_petrol_pump, name='add_petrol_pump'),
    path('add-petrol_pump-ajax/', add_petrol_pump_ajax, name='add_petrol_pump_ajax'),

    path('add-mechanic/', add_mechanic, name='add_mechanic'),
    path('add-mechanic-ajax/', add_mechanic_ajax, name='add_mechanic_ajax'),
    path('update-mechanic/<mechanic_id>', update_mechanic, name='update_mechanic'),
    path('delete-mechanic/<mechanic_id>', delete_mechanic, name='delete_mechanic'),
    path('list-mechanic/', list_mechanic, name='list_mechanic'),

    path('add-vendor/', add_vendor, name='add_vendor'),
    path('add-vendor-ajax/', add_vendor_ajax, name='add_vendor_ajax'),
    path('update-vendor/<vendor_id>', update_vendor, name='update_vendor'),
    path('delete-vendor/<vendor_id>', delete_vendor, name='delete_vendor'),
    path('list-vendor/', list_vendor, name='list_vendor'),
    
    path('update-petrol_pump/<petrol_pump_id>', update_petrol_pump, name='update_petrol_pump'),
    path('delete-petrol_pump/<petrol_pump_id>', delete_petrol_pump, name='delete_petrol_pump'),
    path('list-petrol_pump/', list_petrol_pump, name='list_petrol_pump'),
    
    path('add-station/', add_station, name='add_station'),
    path('add-station-ajax/', add_station_ajax, name='add_station_ajax'),
    path('update-station/<station_id>', update_station, name='update_station'),
    path('delete-station/<station_id>', delete_station, name='delete_station'),
    path('list-station/', list_station, name='list_station'),
    
    path('add-from-station/', add_from_station, name='add_from_station'),
    path('add-from-station-ajax/', add_from_station_ajax, name='add_from_station_ajax'),
    path('update-from-station/<from_station_id>', update_from_station, name='update_from_station'),
    path('delete-from-station/<from_station_id>', delete_from_station, name='delete_from_station'),
    path('list-from-station/', list_from_station, name='list_from_station'),
    
    path('add-district/', add_district, name='add_district'),
    path('add-district-ajax/', add_district_ajax, name='add_district_ajax'),
    path('update-district/<district_id>', update_district, name='update_district'),
    path('delete-district/<district_id>', delete_district, name='delete_district'),
    path('list-district/', list_district, name='list_district'),
    
    path('add-taluka/', add_taluka, name='add_taluka'),
    path('add-taluka-ajax/', add_taluka_ajax, name='add_taluka_ajax'),
    path('update-taluka/<taluka_id>', update_taluka, name='update_taluka'),
    path('delete-taluka/<taluka_id>', delete_taluka, name='delete_taluka'),
    path('list-taluka/', list_taluka, name='list_taluka'),
    
    path('get_buily_code/', get_buily_code, name='get_buily_code'),

    # #delete urls 

    # path('list-company-delete/', list_company_delete, name='list_company_delete'),
    # path('list-company-goods-delete/', list_company_goods_delete, name='list_company_goods_delete'),
    # path('list-goods-company-delete/', list_goods_company_delete, name='list_goods_company_delete'),
    # path('list-agent-delete/', list_agent_delete, name='list_agent_delete'),






    # 
    # 
    # 
    # 
    # 

]
