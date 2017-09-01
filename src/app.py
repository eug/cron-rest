# -*- coding: utf-8 -*-
from flask import Flask, request
from crontab import CronTab
from pretty_cron import prettify_cron
import json
import os
from pathlib import Path


app = Flask(__name__)

@app.route('/')
def home():
    contents = Path(app.root_path + '/index.html').read_text()
    return contents

@app.route('/create')
def create():
    pattern = request.args.get('pattern')
    command = request.args.get('command')
    
    if not command or prettify_cron(pattern) == pattern:
        return json.dumps({
            'status': 'fail',
            'message': 'Some arguments are invalid.'
        })

    cron = CronTab(user=os.getenv('USER'))
    job_id = len(cron)

    job = cron.new(command=command)
    job.setall(pattern)
    cron.write()

    return json.dumps({
        'status':'ok',
        'job': {
            'id': job_id,
            'pattern': pattern,
            'command': command,
            'description': prettify_cron(pattern)
        }
    })

@app.route('/retrieve', defaults={'job_id': -1})
@app.route('/retrieve/id/<int:job_id>')
def retrieve(job_id):

    jobs = []
    cron = CronTab(user=os.getenv('USER'))

    if job_id < 0:
        for i, job in enumerate(cron):
            pattern = job.slices.render()
            jobs.append({
                'id': i,
                'pattern': pattern,
                'command': job.command,
                'description': prettify_cron(pattern)
            })
    elif job_id < len(cron):
        job = cron[job_id]
        pattern = job.slices.render()
        return json.dumps({
            'status': 'ok',
            'job' : {
                'id': job_id,
                'pattern': pattern,
                'command': job.command,
                'description': prettify_cron(pattern)
            }
        })
    else:
        return json.dumps({
            'status': 'fail',
            'message': 'Job ID is invalid.'
        })

    return json.dumps({
        'status': 'ok',
        'jobs' : jobs
    })

@app.route('/update/id/<int:job_id>')
def update(job_id):
    pattern = request.args.get('pattern')
    command = request.args.get('command')

    if not command or prettify_cron(pattern) == pattern:
        return json.dumps({
            'status': 'fail',
            'message': 'Some argument must be provided.'
        })

    cron = CronTab(user=os.getenv('USER'))
    if job_id >= len(cron) or job_id < 0:
        return json.dumps({
            'status': 'fail',
            'message': 'Job ID is invalid.'
        })

    if command:
        cron[job_id].set_command(command)
        
    if prettify_cron(pattern) != pattern:
        cron[job_id].setall(pattern)

    cron.write()

    return json.dumps({
        'status': 'ok',
        'job': {
            'id': job_id,
            'pattern': pattern,
            'command': command,
            'description': prettify_cron(pattern)
        }
    })

@app.route('/delete/id/<int:job_id>')
def delete(job_id):
    cron = CronTab(user=os.getenv('USER'))
    if job_id >= len(cron) or job_id < 0:
        return json.dumps({
            'status': 'fail',
            'message': 'Job ID is invalid.'
        })

    cron.remove(cron[job_id])
    cron.write()

    return json.dumps({'status': 'ok'})

if __name__ == '__main__':
    app.run()
