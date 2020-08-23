from django.shortcuts import render
from django.http import JsonResponse
from django.db.utils import IntegrityError
from .forms import SearchForm
from .models import ProductDetail
import requests


# Create your views here.
def index(request):
    return render(request, "search/index.html", {"form" : SearchForm})


def save_to_database(request):
    import json
    list_of_json = request.POST.getlist("queryset[]", [])
    list_of_json = [ json.loads(item) for item in list_of_json ]

    # print(len(list_of_json))
    for each in list_of_json:
        try:
            obj, created = ProductDetail.objects.update_or_create(**each)
        except IntegrityError:
            product_id = each.pop('product_id')
            ProductDetail.objects.filter(pk=product_id).update(**each)
            print("Duplicate entry : {}".format(product_id))
            
    return JsonResponse({"status" : True})


def get_paytm_data(request):
    list_of_products = list()
    search_query = request.POST.get("query")
    page_num = request.POST.get("page_num")
    url = f"https://search.paytm.com/v2/search?userQuery={ search_query }&page_count={ page_num }&items_per_page=50"

    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        all_product_details = json_response['grid_layout']
        list_of_products = [
            {
                'product_id' : each['product_id'],
                'product' : each['name'],
                'url' : each['url'],
                'image_url': each['image_url'],
                'price' : each['offer_price'],
                'source' : 'Paytm Mall'
            } for each in all_product_details
        ]

        output_json = {
            "status" : True,
            "data" : list_of_products
        }
        return JsonResponse(output_json)
    
    # if not returned above, i.e, Exception Raised
    return JsonResponse({"status" : False, "error" : response.status_code})

def get_shopclues_data(request):
    search_query = request.POST.get("query")
    page_num = request.POST.get("page_num")
    list_of_products = []
    start_page = int(page_num)
    for i in range(start_page, start_page + 5):
        url = f"http://api.shopclues.com/api/v11/search?q={ search_query }\
            &z=1&key=d12121c70dda5edfgd1df6633fdb36c0&page={ str(i) }"
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if "products" in json_response.keys():
                all_product_details = json_response['products']
                for each in all_product_details:
                    list_of_products.append(
                        {
                            'product_id' : each['product_id'],
                            'product' : each['product'],
                            'url' : each['product_url'],
                            'image_url': each['image_url'],
                            'price' : each['price'],
                            'source' : 'Shopclues'
                        }
                    )
            
    if list_of_products:

        output_json = {
            "status" : True,
            "data" : list_of_products
        }
        return JsonResponse(output_json)

    # if not returned above, i.e, Exception Raised
    return JsonResponse({"status" : False, "error" : response.status_code})


def get_tata_cliq(request):
    search_query = request.POST.get("query")
    page_num = request.POST.get("page_num")
    page_num = int(page_num) - 1
    url = f"https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/searchProducts/?searchText={ search_query }\
        %3Arelevance%3AinStockFlag%3Atrue&isKeywordRedirect=false\
        &isKeywordRedirectEnabled=true&channel=WEB&isMDE=true\
        &isTextSearch=false&isFilter=false&page={ str(page_num) }\
            &isPwa=true&pageSize=50&typeID=all"

    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['status'] == "Success":
            try:
                all_product_details = json_response['searchresult']
                list_of_products = [
                    {
                        'product_id' : each['productId'],
                        'product' : each['productname'],
                        'url' : "https://www.tatacliq.com" + each['webURL'],
                        'image_url': "https:" + each['imageURL'],
                        'price' : each['price']['sellingPrice']['doubleValue'],
                        'source' : 'Tata Cliq'
                    } for each in all_product_details
                ]
                
                output_json = {
                    "status" : True,
                    "data" : list_of_products
                }
                return JsonResponse(output_json)
            except KeyError:
                pass

    return JsonResponse({"status" : False, "error" : response.status_code})