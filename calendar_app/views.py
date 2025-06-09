from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import calendar
from .models import WorkLog, Memo, Event, MenuPhoto, Suggestion, CafeteriaMenu
from .forms  import CafeteriaMenuForm, MenuPhotoForm
from suggestions.models import Suggestion
from used_books.models import UsedBook
from calendar import monthrange
from WeatherLiveAPI.weather_video_data import get_weather_data
from django.db.models import Count

def calendar_view(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

    if year and month:
        try:
            current_date = date(int(year), int(month), 1)
        except ValueError:
            current_date = date.today().replace(day=1)
    else:
        month_str = request.GET.get('month')
        if month_str:
            try:
                current_date = datetime.strptime(month_str, "%Y-%m").date()
            except ValueError:
                current_date = date.today().replace(day=1)
        else:
            current_date = date.today().replace(day=1)

    year, month = current_date.year, current_date.month

    prev_month_date = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    next_month_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    prev_month = prev_month_date.strftime("%Y-%m")
    next_month = next_month_date.strftime("%Y-%m")

    cal = calendar.Calendar(firstweekday=6)
    calendar_weeks = cal.monthdatescalendar(year, month)

    calendar_days = []
    for week in calendar_weeks:
        for d in week:
            calendar_days.append({
                'date': d,
                'work_logs': WorkLog.objects.filter(date=d),
                'events': Event.objects.filter(date=d),
                'menus': CafeteriaMenu.objects.filter(date=d),
                'memos': Memo.objects.filter(date=d),
            })

    date_param = request.GET.get('date')
    if date_param:
        sel_date = date.fromisoformat(date_param)
        selected_logs = WorkLog.objects.filter(date=sel_date)
        selected_events = Event.objects.filter(date=sel_date)
        selected_memos = Memo.objects.filter(date=sel_date)
        menu, _ = CafeteriaMenu.objects.get_or_create(date=sel_date)
        mform = CafeteriaMenuForm(instance=menu)
        pform = MenuPhotoForm()
        selected_photos = menu.photos.all()
    else:
        sel_date = None
        selected_logs = selected_events = selected_memos = []
        mform = pform = None
        selected_photos = []

    recent_suggestions = Suggestion.objects.order_by('-created_at')[:5]
    recent_books = UsedBook.objects.order_by('-created_at')[:5]
    weather_data = get_weather_data()

    # 🔥 여기서 드롭다운용 리스트도 추가
    years = range(2000, 2099)
    months = range(1, 13)

    return render(request, 'calendar_app/calendar.html', {
        'calendar_weeks': calendar_weeks,
        'calendar_days': calendar_days,
        'current_month': current_date,
        'prev_month': prev_month,
        'next_month': next_month,
        'selected_date': sel_date,
        'selected_logs': selected_logs,
        'selected_events': selected_events,
        'selected_memos': selected_memos,
        'mform': mform,
        'pform': pform,
        'selected_photos': selected_photos,
        'recent_suggestions': recent_suggestions,
        'recent_books': recent_books,
        'weather': weather_data,
        'years': years,   # ✅
        'months': months, # ✅
    })




@require_POST
@csrf_exempt
def add_worklog(request):
    date_str = request.POST.get('date')
    hours    = request.POST.get('hours')
    if not date_str or not hours:
        return JsonResponse({'status':'error','message':'날짜와 시간을 보내주세요.'}, status=400)
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({'status':'error','message':'잘못된 날짜 형식입니다.'}, status=400)
    log = WorkLog.objects.create(date=d, hours_worked=hours)
    return JsonResponse({'status':'ok','date':date_str,'hours':str(log.hours_worked),'id':log.id})

@require_POST
@csrf_exempt
def delete_worklog(request):
    log_id = request.POST.get('id')
    if not log_id:
        return JsonResponse({'status':'error','message':'ID가 없습니다.'}, status=400)
    try:
        log = WorkLog.objects.get(id=log_id)
        log.delete()
        return JsonResponse({'status':'ok','id':log_id})
    except WorkLog.DoesNotExist:
        return JsonResponse({'status':'error','message':'존재하지 않는 기록입니다.'}, status=404)

@require_POST
@csrf_exempt
def add_memo(request):
    date_str = request.POST.get('date')
    note     = request.POST.get('note','').strip()
    if not date_str or not note:
        return JsonResponse({'status':'error','message':'날짜와 메모를 보내주세요.'}, status=400)
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({'status':'error','message':'잘못된 날짜 형식입니다.'}, status=400)
    memo = Memo.objects.create(date=d, note=note)
    return JsonResponse({'status':'ok','date':date_str,'note':memo.note,'id':memo.id})

@require_POST
@csrf_exempt
def delete_memo(request):
    memo_id = request.POST.get('id')
    if not memo_id:
        return JsonResponse({'status':'error','message':'ID가 없습니다.'}, status=400)
    try:
        m = Memo.objects.get(id=memo_id)
        m.delete()
        return JsonResponse({'status':'ok','id':memo_id})
    except Memo.DoesNotExist:
        return JsonResponse({'status':'error','message':'해당 메모를 찾을 수 없습니다.'}, status=404)

# ── AJAX endpoints for cafeteria menu ──

@require_POST
def add_menu_text(request):
    date_str = request.POST.get('date')
    text     = request.POST.get('menu_text','').strip()
    if not date_str:
        return JsonResponse({'status':'error','message':'날짜가 없습니다.'}, status=400)
    menu, _ = CafeteriaMenu.objects.get_or_create(date=date.fromisoformat(date_str))
    menu.menu_text = text
    menu.save()
    return JsonResponse({'status':'ok','menu_text':menu.menu_text})

@require_POST
def upload_menu_photo(request):
    date_str = request.POST.get('date')
    pic      = request.FILES.get('image')
    if not date_str or not pic:
        return JsonResponse({'status':'error','message':'날짜/사진이 없습니다.'}, status=400)
    menu, _ = CafeteriaMenu.objects.get_or_create(date=date.fromisoformat(date_str))
    photo = MenuPhoto.objects.create(menu=menu, image=pic)
    return JsonResponse({
        'status':'ok',
        'photo_url': photo.image.url
    })
def menu_detail(request, year, month, day):
    """
    메뉴 폼(GET/POST)은 AJAX로 처리하고,
    일반 요청(GET/POST)이 들어오면 달력 뷰로 리다이렉트 합니다.
    """
    # year, month, day → YYYY-MM, YYYY-MM-DD 포맷
    month_str = f"{year:04d}-{month:02d}"
    date_str  = f"{year:04d}-{month:02d}-{day:02d}"

    # 달력 뷰 URL에 쿼리스트링을 붙여 리다이렉트
    url = reverse('calendar_app:calendar')
    return redirect(f"{url}?month={month_str}&date={date_str}")

@require_POST
def delete_menu_text(request):
    date_str = request.POST.get('date')
    if not date_str:
        return JsonResponse({'status':'error','message':'날짜가 없습니다.'}, status=400)
    menu = get_object_or_404(CafeteriaMenu, date=date.fromisoformat(date_str))
    menu.menu_text = ''
    menu.save()
    return JsonResponse({'status':'ok'})

@require_POST
def delete_menu_photo(request):
    photo_id = request.POST.get('photo_id')
    if not photo_id:
        return JsonResponse({'status':'error','message':'사진 ID가 없습니다.'}, status=400)
    photo = get_object_or_404(MenuPhoto, id=photo_id)
    photo.delete()
    return JsonResponse({'status':'ok','photo_id': photo_id})

def submit_suggestion(request):
    if request.method == 'POST':
        content = request.POST.get('suggestion', '')
        if content:
            Suggestion.objects.create(content=content)
    return redirect('calendar')

def suggestion_community(request):
    if request.method == 'POST':
        content = request.POST.get('suggestion', '')
        if content:
            Suggestion.objects.create(content=content)
        return redirect('suggestion_community')

    suggestions = Suggestion.objects.order_by('-created_at')
    return render(request, 'calendar_app/suggestions.html', {
        'suggestions': suggestions,
    })

