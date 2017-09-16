# cron-rest
A simple REST API for Cron written in Python

## Install
```
# python3 setup.py install
```

## Run
```
$ python3 src/app.py
```

## API
* [Create](#creating-a-job)
* [Retrieve](#retrieving-jobs)
* [Update](#updating-a-job)
* [Delete](#deleting-a-job)

### Creating a job
`POST /create`

**Request**
```bash
curl -X POST
     -H "Content-Type:application/x-www-form-urlencoded; charset=UTF-8"\
     -d 'pattern=1 * * * *&command=echo "Hello World"'\
     http://localhost:5000/create
```

**Response**
```bash
{
  "job": {
    "id": 6,
    "pattern": "1 * * * *",
    "command": "echo \"Hello World\"",
    "description": "At 1 minutes past every hour of every day"
  },
  "status": "ok",
  "message": "Job successfully created."
}
```

### Retrieving jobs
`GET /retrieve[/id/{id}]`

**Request**
```bash
curl -X GET http://localhost:5000/retrieve/id/1
```

**Response**
```bash
{
  "jobs": [{
    "id": 1,
    "pattern": "1 * * * *",
    "command": "echo \"Hello World!\";",
    "description": "At 1 minutes past every hour of every day"
  }],
  "status": "ok",
  "message": "Job retrieved successfully"
}
```

### Updating a job
`POST /update/id/{id}`

**Request**
```bash
curl -X POST\
     -H "Content-Type:application/x-www-form-urlencoded; charset=UTF-8"\
     -d 'pattern=2 * * * *&command=echo "Hello World"'\
     http://localhost:5000/update/id/1
```

**Response**
```bash
{
  "job": {
    "id": 1,
    "pattern": "2 * * * *",
    "command": "echo \"Hello World!\";",
    "description": "At 2 minutes past every hour of every day"
  },
  "status": "ok",
  "message": "Job updated successfully."
}
```

### Deleting a job
`DELETE /delete/id/{id}`

**Request**
```bash
curl -X DELETE http://localhost:5000/delete/id/1
```

**Response**
```bash
{
  'status': 'ok',
  'message': 'Job deleted successfully.'
}
```

## License
MIT