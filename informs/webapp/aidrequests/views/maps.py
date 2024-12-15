from django.conf import settings
import httpx
from icecream import ic
# from decimal import Decimal


def staticmap_aid(width=600, height=400, zoom=13,
                  fieldop_lat=0.0, fieldop_lon=0.0,
                  aid1_lat=0.0, aid1_lon=0.0):

    # ic(type(aid1_lat), type(aid1_lon))
    # ic(type(fieldop_lat), type(fieldop_lon))
    center_lat = (fieldop_lat + aid1_lat) / 2
    center_lon = (fieldop_lon + aid1_lon) / 2

    pin_instances = [
        f"default|co008000|lcFFFFFF||'OP'{fieldop_lon} {fieldop_lat}",
        f"default|coFFFF00|lc000000||'AID'{aid1_lon} {aid1_lat}"
    ]

    url = settings.AZURE_MAPS_STATIC_URL
    params = {
        'subscription-key': settings.AZURE_MAPS_KEY,
        'api-version': '2024-04-01',
        'layer': 'basic',
        'style': 'main',
        'zoom': zoom,
        'center': f'{center_lon},{center_lat}',
        'width': width,
        'height': height,
        'pins': pin_instances,
        'path': f'lcFF1493||{fieldop_lon} {fieldop_lat}|{aid1_lon} {aid1_lat}'
    }
    try:
        response = httpx.get(url, params=params)
    except Exception as e:
        ic(f"Error: {e}")

    if response.content.startswith(b'\x89PNG'):
        return response.content
    else:
        return None


def calculate_zoom(distance=0):
    if distance <= 0.4:
        return 16
    if distance <= 1:
        return 15
    if distance <= 2:
        return 14
    elif distance <= 4:
        return 13
    elif distance <= 10:
        return 12
    elif distance <= 20:
        return 11
    elif distance <= 35:
        return 10
    elif distance <= 60:
        return 9
    elif distance <= 120:
        return 8
    elif distance <= 300:
        return 7
    elif distance <= 500:
        return 6
    elif distance <= 1000:
        return 5
    elif distance <= 2000:
        return 4
    elif distance <= 3000:
        return 3
    else:
        return 2
