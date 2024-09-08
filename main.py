import flet as ft
from pathlib import Path

from parse_link_city import parse_link
from parse_weather import parse_weather
window_size = [800, 400]
window_pos = [220, 520]
info_user_location = {'city':'',
                      'district':'',
                      'region':'',
                      'country':''}
data_weather = {}
weather_bar = ft.Row()
def main(page: ft.Page):

    global weather_bar
    page.window.width = window_size[0]
    page.window.height = window_size[1]
    page.window.top = window_pos[0]
    page.window.left = window_pos[1]

    icon_url = Path(__file__).parent / 'resource/icon.ico'  # іконка вікна
    page.window.icon = icon_url

    page.title = 'Погода'

    def create_zero_tab(data = None):
        items = []
        if data is None:
            day_str =ft.Row([ft.Text('.')], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            day_int = ft.Row([ft.Text('..')], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            month_str = ft.Row([ft.Text('...')], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            t_min = ft.Row([ft.Text('...')], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            t_max = ft.Row([ft.Text('...')], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            for i in range(1,8):
                items.append(ft.Container(content=
                    ft.Column([day_str,day_int, month_str,
                               ft.Row([ft.Column([ft.Text('min'),t_min]),
                                       ft.Column([ft.Text('max'),t_max])], alignment=ft.MainAxisAlignment.SPACE_AROUND)],
                              alignment=ft.MainAxisAlignment.SPACE_AROUND)

                ,bgcolor= ft.colors.GREY, border_radius=20, width= 100, height=200
                                          ))
        else:
            for i,e in zip(range(1, 8),data):
                day_str = ft.Row([ft.Text(data[e][0])], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                day_int = ft.Row([ft.Text(data[e][1])], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                month_str = ft.Row([ft.Text(data[e][2])], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                t_min = ft.Row([ft.Text(data[e][4])], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                t_max = ft.Row([ft.Text(data[e][6])], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                items.append(ft.Container(content=
                                          ft.Column([day_str, day_int, month_str,
                                                     ft.Row([ft.Column([ft.Text('min'), t_min]),
                                                             ft.Column([ft.Text('max'), t_max])],
                                                            alignment=ft.MainAxisAlignment.SPACE_AROUND)],
                                                    alignment=ft.MainAxisAlignment.SPACE_AROUND)

                                          , bgcolor=ft.colors.GREY, border_radius=20, width=100, height=200
                                          ))
        return items

    def get_weather(e):
        global data_weather
        global weather_bar
        weather_bar.controls.clear()
        city_input = weather_search_input.value.strip()
        # city_input = 'Юрівка,Любарський район,Житомирська область,Україна'
        link_city = next(parse_link(city_input))
        if link_city.startswith('NoFind:'):
            shake_bar = ft.SnackBar(content = ft.Text(f'{link_city[8:]}: Перевірте введені дані'),open=True)
            page.overlay.append(shake_bar)
            page.update()
        elif link_city.startswith('Data:'):
            data_weather = parse_weather(link_city[5:])
            weather_bar.controls.extend(create_zero_tab(data_weather))
            page.update()

    weather_bar = ft.Row(create_zero_tab())
    weather_search_start = ft.Text(value='Показати погоду в :')
    weather_search_input = ft.TextField(label=f'Write your city')
    start_search = ft.TextButton(text='Пошук', on_click=get_weather)
    page.add(ft.Column([ft.Row([weather_search_start,weather_search_input], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([start_search], alignment=ft.MainAxisAlignment.CENTER),
                        weather_bar,
                        ]))

ft.app(target=main)