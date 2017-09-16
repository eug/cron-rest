# -*- coding: utf-8 -*-
import json
import os
from crontab import CronTab
from flask import Flask, request
from pathlib import Path
from pretty_cron import prettify_cron


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return Path(app.root_path + '/index.html').read_text()

@app.route('/create', methods=['POST'])
def create():
    pattern = request.form['pattern']
    command = request.form['command']

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
        'status': 'ok',
        'message': 'Job successfully created.',
        'job': {
            'id': job_id,
            'pattern': pattern,
            'command': command,
            'description': prettify_cron(pattern)
        }
    })

@app.route('/retrieve', methods=['GET'], defaults={'job_id': -1})
@app.route('/retrieve/id/<int:job_id>', methods=['GET'])
def retrieve(job_id):

    jobs = []
    cron = CronTab(user=os.getenv('USER'))

    if job_id < 0:
        for i, job in enumerate(cron):
            pattern = job.slices.render()
            command = job.command
            description = prettify_cron(pattern)
            jobs.append({
                'id': i,
                'pattern': pattern,
                'command': command,
                'description': description
            })
        return json.dumps({
            'status': 'ok',
            'message': 'Jobs retrieved successfully',
            'jobs' : jobs
        })
    elif job_id < len(cron):
        job = cron[job_id]
        pattern = job.slices.render()
        command = job.command
        description = prettify_cron(pattern)
        return json.dumps({
            'status': 'ok',
            'message': 'Job retrieved successfully',
            'jobs' : [{
                'id': job_id,
                'pattern': pattern,
                'command': command,
                'description': description

            }]
        })

    return json.dumps({
        'status': 'fail',
        'message': 'Job ID is invalid.'
    })

@app.route('/update/id/<int:job_id>', methods=['POST'])
def update(job_id):
    pattern = request.form['pattern'] if 'pattern' in request.form else None
    command = request.form['command'] if 'command' in request.form else None
    description = ''

    if not command and prettify_cron(pattern) == pattern:
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

    if not command:
        command = cron[job_id].command
    cron[job_id].set_command(command)

    if pattern and prettify_cron(pattern) != pattern:
        cron[job_id].setall(pattern)
        description = prettify_cron(pattern)
    else:
        pattern = cron[job_id].slices.render()

    cron.write()

    return json.dumps({
        'status': 'ok',
        'message': 'Job updated successfully.',
        'job': {
            'id': job_id,
            'pattern': pattern,
            'command': command,
            'description': description
        }
    })

@app.route('/delete/id/<int:job_id>', methods=['DELETE'])
def delete(job_id):
    cron = CronTab(user=os.getenv('USER'))

    if job_id >= len(cron) or job_id < 0:
        return json.dumps({
            'status': 'fail',
            'message': 'Job ID is invalid.'
        })

    cron.remove(cron[job_id])
    cron.write()

    return json.dumps({
        'status': 'ok',
        'message': 'Job deleted successfully.'
    })

if __name__ == '__main__':
    app.run()
