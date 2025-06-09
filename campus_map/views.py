from django.shortcuts import render

def campus_map_view(request):
    return render(request, 'campus/campus_map.html')

def bus_map_view(request):
    return render(request, 'campus/bus_map.html')
def bus_map_view(request): # 버스 마커 기능
    markers = [
        {'x': 1584, 'y': 1520, 'label': '정류장 A'},
        {'x': 1882, 'y': 1140, 'label': '정류장 B'},
        {'x': 1200, 'y': 862, 'label': '정류장 C'},
        {'x': 810,  'y': 384,  'label': '정류장 D'},
        {'x': 362,  'y': 530,  'label': '정류장 E'},
    ]
    return render(request, 'campus/bus_map.html', {'markers': markers})

def campus_map_view(request):
    markers = [
        {'x': 15.93, 'y': 34.09, 'label': '기숙사 식당'},   # 첫 번째 마커
        {'x': 45.53, 'y': 41.11, 'label': '학생 식당'},     # 두 번째 마커
        {'x': 82.47, 'y': 58.65, 'label': '교직원 식당'}, # 세 번째 마커
        {'x': 60.47, 'y': 69.12, 'label': '비즈니스 식당'},       # 네 번째 마커
    ]
    return render(request, 'campus/campus_map.html', {'markers': markers})