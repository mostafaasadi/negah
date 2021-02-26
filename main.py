from datetime import datetime
from selenium import webdriver
from flask import Flask, request, render_template, make_response


app = Flask(__name__)


def screenshot(link):
    d = datetime.timestamp(datetime.now())
    resd = {}
    size = [
        {'mode': 'mobile', 'width': 480, 'height': 854},
        {'mode': 'desktop', 'width': 1920, 'height': 1080},
        {'mode': 'tablet', 'width': 960, 'height': 540}
    ]
    driver.get(link)
    for i in size:
        try:
            dst = 'sc/{}_{}.png'.format(i['mode'], d)
            driver.set_window_size(i['width'], i['height'])
            driver.save_screenshot('static/' + dst)
            resd[i['mode']] = dst
        except Exception as e:
            print(e)

    return resd


@app.route('/')
def static_page():
    resp = make_response(render_template('index.html'))
    return resp


@app.route('/result', methods=['POST'])
def result():
    try:
        linkt = request.form['linkt']
    except Exception:
        pass
        # TODO: error
    resd = screenshot(linkt)
    resp = make_response(render_template('result.html', scu=resd))
    return resp


def main():
    global options, driver
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('chromedriver', options=options)
    app.run(host='0.0.0.0', debug=True, port='8080')


if __name__ == '__main__':
    main()
