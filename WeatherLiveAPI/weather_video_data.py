import requests

def get_weather_data(lat=36.6424, lon=127.4889):
    API_KEY = '96cac1e3452c83258d58f8a071636b85'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()
        condition = data['weather'][0]['main']

        # ✅ weather condition -> 파일명 매핑
        video_mapping = {
            'Clear': 'sunny.mp4',
            'Clouds': 'cloud.mp4',
            'Rain': 'rain.mp4',
            'Snow': 'snow.mp4',
        }

        video_filename = video_mapping.get(condition, 'cloud.mp4')  # 기본 fallback도 설정

        return {
            'condition': condition,
            'video_path': f"videos/{video_filename}"
        }

    except Exception as e:
        print("날씨 API 오류:", e)
        return {
            'condition': 'Default',
            'video_path': 'videos/cloud.mp4'  # 오류 시 기본값
        }