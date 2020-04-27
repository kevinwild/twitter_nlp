if __name__ == '__main__':
    import os
    import settings

    border = '===================================================================================='
    lines = '---'
    command = settings.CONFIG.get('python_shell_cmd') + ' -m http.server'

    print(border)
    print('  Visit the URL displayed below')
    print(border)
    print(lines)
    print(lines + ' -- To Exit Program: press ctrl+c')
    print(lines + ' ** If the server fails on start, check to see if you have any other processes running on \n' +
          lines + ' ** port 8000. Otherwise you can start a static http server using PHP or Node.js within the project directory. \n' +
          lines + ' ** visit the http servers root address to view the report: ie localhost:8000 or 127.0.0.1:8000 or 0.0.0.0:8000 \n' +
          lines + ' ** or another local domain using port 8000.')
    print(lines)
    print(border)

    os.system(command)
