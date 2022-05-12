from requests import post
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    data = post('https://inf2086.ru/trains_timetable_api/timetable', data='340yk034k4f').text
    if data == 'timetable_not_ready': data = open('last.txt', 'r', encoding='UTF-8').read()
    else: print('req')
    with open('last.txt', 'w', encoding='UTF-8') as file:
        file.write(data)
    return render_template("first.html", title="Главная страница", trains=get_data(data))


def time(tm):
    new = tm.split(':')
    return int(new[0]) * 60 + int(new[1])


def normal(sp):
    result = list()
    for i in sp:
        new = []
        for j in i:
            if '-' not in j: new.append(j)
            else:
                name = j.split('-')
                for n in name:
                    new.append(' '.join(n.split('+')))
        result.append(new)
    return result


def stop(dt):
    if dt == []: return []
    stp = str(time(dt[-1]) - time(dt[-2])) + ' мин'
    return dt + [stp]


def get_data(req):
    data = [stop(x.split()[1:]) for x in req.split('\n')]
    if data[-1] == []: del data[-1]
    data = sorted(data, key=lambda x: time(x[3]))
    return normal(data)


app.run('', 8092, debug=True)