def run_gunicorn_0_16_1_bind(projectname):
    from subprocess import call
    call(["gunicorn", "--worker-class", "socketio.sgunicorn.GeventSocketIOWorker", "--bind", "0.0.0.0:8000" , projectname + ".wsgi:application", "-w", "1",  "--log-file", "-"])

run_gunicorn_0_16_1_bind("i2c")
