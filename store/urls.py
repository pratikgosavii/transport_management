from django.urls import path

from .views import *
from store import views

urlpatterns = [

    path('get-consignor-ajax/', get_consignor_ajax, name="get_consignor_ajax"),
    # path('get-goods_company-ajax/', get_goods_company_ajax, name="get_goods_company_ajax"),
    # path('get-agent_company-ajax/', get_agent_company_ajax, name="get_agent_company_ajax"),

    path('add-company/', add_company, name='add_company'),
    path('update-company/<company_id>', update_company, name='update_company'),
    path('delete-company/<company_id>', delete_company, name='delete_company'),
    path('list-company/', list_company, name='list_company'),

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
    path('update-truck-other/<truck_owner_id>', update_truck_owner, name='update_truck_owner'),
    path('delete-truck-other/<truck_owner_id>', delete_truck_owner, name='delete_truck_owner'),
    path('list-truck-other/', list_truck_owner, name='list_truck_owner'),
    
    path('add-onaccount/', add_onaccount, name='add_onaccount'),
    path('update-onaccount/<onaccount_id>', update_onaccount, name='update_onaccount'),
    path('delete-onaccount/<onaccount_id>', delete_onaccount, name='delete_onaccount'),
    path('list-onaccount/', list_onaccount, name='list_onaccount'),
    
    path('add-station/', add_station, name='add_station'),
    path('update-station/<station_id>', update_station, name='update_station'),
    path('delete-station/<station_id>', delete_station, name='delete_station'),
    path('list-station/', list_station, name='list_station'),
    
    path('add-district/', add_district, name='add_district'),
    path('update-district/<district_id>', update_district, name='update_district'),
    path('delete-district/<district_id>', delete_district, name='delete_district'),
    path('list-district/', list_district, name='list_district'),
    
    path('add-taluka/', add_taluka, name='add_taluka'),
    path('update-taluka/<taluka_id>', update_taluka, name='update_taluka'),
    path('delete-taluka/<taluka_id>', delete_taluka, name='delete_taluka'),
    path('list-taluka/', list_taluka, name='list_taluka'),

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
