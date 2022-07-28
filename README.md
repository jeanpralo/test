## Fergus Challenge

### Run app with Docker

This app run with docker so it must be installed locally.

In order to boot up app simply run the run.sh bash script in this repo. 

`$ bash ./run.sh`

### Run app locally

Alternatively, you can run it locally if you wish.

```bash
$ python3 -m venv venv
$ . venv/bin/activate
# install pip requirement
$ pip install -r requirements.txt
# make sure we add local project to path
$ export PYTHONPATH=$PYTHONPATH:.
# create db, schema and seed data
$ alembic upgrade head
# boot up app
$ python fergus/app.py
```


### Api Documentation

#### List jobs:

```bash
curl 'http://localhost:5000/jobs' | jq .
[
  {
    "job_id": "ab494e8c-ecaf-4238-8029-10884076ae30",
    "status": "completed",
    "created_at": "2022-07-02T13:34:16",
    "contact_name": "Christopher Jacobs",
    "phone": "0639868907",
    "description": "Trial drop test field forward strategy size world."
  },
  {
    "job_id": "7cacf5fc-297e-438f-acaf-7f0020749bac",
    "status": "scheduled",
    "created_at": "2022-06-30T14:35:43",
    "contact_name": "Rhonda Morgan",
    "phone": "(178)009-3106x55672",
    "description": "Important news seek story."
  }
]
```

### List job and sort by a column desc or asc
It is also possible to sort by a different column, replace created_at by status for example.
```bash
$ curl 'http://localhost:5000/jobs?sort=created_at:desc' | jq .
[
  {
    "job_id": "4bfdd3f2-8fd5-437d-8eb7-46da7524cbef",
    "status": "completed",
    "created_at": "2022-07-27T05:55:36",
    "contact_name": "Jacob Murray",
    "phone": "001-671-909-9800",
    "description": "Film turn in friend."
  },
  {
    "job_id": "4b245a4b-9d6d-4043-9d8d-aa29702a557d",
    "status": "invoicing",
    "created_at": "2022-07-22T04:54:41",
    "contact_name": "Thomas Gray",
    "phone": "(141)144-9268x09112",
    "description": "Student fact alone institution hope."
  },
  ...
]

$ curl 'http://localhost:5000/jobs?sort=created_at:asc' | jq . 
[
  {
    "job_id": "1015c835-208a-414b-8eab-4e85a2e9ad29",
    "status": "active",
    "created_at": "2022-07-01T20:08:24",
    "contact_name": "Kelly Fernandez",
    "phone": "001-698-781-8720x153",
    "description": "Employee official husband."
  },
  {
    "job_id": "7aad8bb5-07ea-4840-ac9f-4b3650ac05c8",
    "status": "invoicing",
    "created_at": "2022-07-02T03:39:49",
    "contact_name": "Jeffrey Nolan",
    "phone": "662.814.4955x2362",
    "description": "Mouth size cut work its church miss agreement."
  },
  ...
]
```


### Filter a job by a column
Can use any column that must match the value exactly.
```bash
curl 'http://localhost:5000/jobs?status=invoicing' | jq .  
[
  {
    "job_id": "4b245a4b-9d6d-4043-9d8d-aa29702a557d",
    "status": "invoicing",
    "created_at": "2022-07-22T04:54:41",
    "contact_name": "Thomas Gray",
    "phone": "(141)144-9268x09112",
    "description": "Student fact alone institution hope."
  },
  {
    "job_id": "7aad8bb5-07ea-4840-ac9f-4b3650ac05c8",
    "status": "invoicing",
    "created_at": "2022-07-02T03:39:49",
    "contact_name": "Jeffrey Nolan",
    "phone": "662.814.4955x2362",
    "description": "Mouth size cut work its church miss agreement."
  }
]
```


#### View a job, detail and notes:
```bash
curl 'http://localhost:5000/job/ab494e8c-ecaf-4238-8029-10884076ae30' | jq .
{
  "job_id": "ab494e8c-ecaf-4238-8029-10884076ae30",
  "status": "completed",
  "created_at": "2022-07-02T13:34:16",
  "contact_name": "Christopher Jacobs",
  "phone": "0639868907",
  "description": "Trial drop test field forward strategy size world.",
  "notes": []
}
```


#### Change a job status

This will simply reply 204 or 400 if invalid payload.

```bash
curl -XPATCH 'http://localhost:5000/job/ab494e8c-ecaf-4238-8029-10884076ae30' -H 'Content-Type: application/json' -d '{"status": "scheduled"}'

curl -XPATCH 'http://localhost:5000/job/ab494e8c-ecaf-4238-8029-10884076ae30' -H 'Content-Type: application/json' -d '{"status": "to priced"}'

```

### Add a note

```bash
$ curl -XPOST 'http://localhost:5000/job/47386c1a-fb51-4ffa-956c-82c566afb740/note' -H 'Content-Type: application/json' -d '{"data": "Creation message."}'
{"note_id": "fde8ecd6-b591-46e5-ace2-149a2a08b1fb"}
# view the job
$ curl 'http://localhost:5000/job/47386c1a-fb51-4ffa-956c-82c566afb740' | jq .                                                                            
{
  "job_id": "47386c1a-fb51-4ffa-956c-82c566afb740",
  "status": "invoicing",
  "created_at": "2022-07-28T02:24:43.945073",
  "contact_name": "Holly Bolton",
  "phone": "677-828-7388x747",
  "description": "Authority book eye town.",
  "notes": [
    {
      "note_id": "fde8ecd6-b591-46e5-ace2-149a2a08b1fb",
      "data": "Creation message."
    }
  ]
}

```

### Update a note

```bash
$curl -XPATCH 'http://localhost:5000/note/fde8ecd6-b591-46e5-ace2-149a2a08b1fb' -H 'Content-Type: application/json' -d '{"data": "Updated note."}'

# view updated note
$ curl 'http://localhost:5000/job/47386c1a-fb51-4ffa-956c-82c566afb740' | jq .                                                                     
{
  "job_id": "47386c1a-fb51-4ffa-956c-82c566afb740",
  "status": "invoicing",
  "created_at": "2022-07-28T02:24:43.945073",
  "contact_name": "Holly Bolton",
  "phone": "677-828-7388x747",
  "description": "Authority book eye town.",
  "notes": [
    {
      "note_id": "fde8ecd6-b591-46e5-ace2-149a2a08b1fb",
      "data": "Updated note."
    }
  ]
}

```

