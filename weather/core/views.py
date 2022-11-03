from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def get_html_content(request):
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/44.0.2403.157 Safari/537.36"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = "en-US,en;q=0.5"
    session.headers['Content-Language'] = "en-US,en;q=0.5"
    html_content = session.get(f'https://yandex.ru/pogoda/{city}').text
    return html_content


def home(request):
    context = dict()
    if 'city' in request.GET:
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        context['region'] = soup.find(
            "h1",
            attrs={"class": "title title_level_1 header-title__title"}).text
        context['temp_now'] = soup.find(
            "span",
            attrs={"class": "temp__value temp__value_with-unit"}).text
        context['time'] = soup.find(
            "time",
            attrs={"class": "time fact__time"}).text[:12]
        context['weather'] = soup.find(
            "div",
            attrs={"class": "link__condition day-anchor i-bem"}).text
        context['wind'] = soup.find(
            "span",
            attrs={"class": "wind-speed"}).text
        context['direction_of_wind'] = soup.find(
            "abbr",
            attrs={"class": "icon-abbr"}).text

    return render(request, 'home.html', {'context': context})
