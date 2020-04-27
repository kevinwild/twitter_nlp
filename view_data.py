

def view():
    import webbrowser
    import os

    print('Opening browser to display chart data')
    filename = os.path.join('view/index.html')
    webbrowser.open('file://' + os.path.realpath(filename))


if __name__ == '__main__':
    view()
