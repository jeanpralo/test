import logging
import json
import uuid
import sys

from faker import Faker
from faker.providers import DynamicProvider
from flask import Flask, request
from sqlalchemy.orm import Query
from datetime import datetime as dt

from fergus.db.models.jobs import Jobs
from fergus.db.models.notes import Notes
from fergus.db.db import Db


fake = Faker()
job_status = DynamicProvider(
    provider_name="job_status",
    elements=["scheduled", "active", "invoicing", "to priced", "completed"],
)
fake.add_provider(job_status)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
with open('config.json') as config:
    _app_config = json.load(config)


class ApiJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


def render_json(data, status_code: int = 200):
    return json.dumps(data, cls=ApiJsonEncoder), status_code, {"ContentType": "application/json"}


@app.route('/jobs', methods=['GET'])
def list_jobs():
    # TODO: add filter
    res = []
    request_args = dict(request.args)
    sort = request_args.pop("sort", None)
    with Db() as session:
        jobs_query = Query(Jobs).with_session(session)
        jobs_query = Jobs.sort_job_query(jobs_query, sort)
        jobs_query = Jobs.filter_job_query(jobs_query, request_args)
        jobs = jobs_query.all()
        res = [j.to_dict() for j in jobs]

    return render_json(res)


# Not required but just for testing purposes.
@app.route('/job', methods=['POST'])
def create_job():
    job_id = str(uuid.uuid4())
    note_id = str(uuid.uuid4())
    with Db() as session:
        job = Jobs(
            job_id=job_id,
            status=fake.job_status(),
            contact_name=fake.name(),
            phone=fake.phone_number(),
            description=fake.sentence(),
            created_at=dt.utcnow()
        )
        note = Notes(
            note_id=note_id,
            job_id=job_id,
            data=fake.sentence()
        )
        session.add(job)
        session.add(note)
        session.commit()

    return render_json({'job_id': job_id})


@app.route('/job/<string:job_id>', methods=['GET'])
def view_job(job_id):
    with Db() as session:
        job = Query(Jobs).with_session(session).filter(Jobs.job_id == job_id).first()

        if not job:
            return render_json(None, 404)

        res = job.to_dict()
        notes = []
        _notes = Query(Notes).with_session(session).filter(Notes.job_id == job_id).all()
        if _notes:
            notes = [_note.to_dict() for _note in _notes]
        res['notes'] = notes

    return render_json(res)


@app.route('/job/<string:job_id>', methods=['PATCH'])
def edit_job(job_id):
    with Db() as session:
        job = Query(Jobs).with_session(session).filter(Jobs.job_id == job_id).first()
        valid_statuses = ["scheduled", "active", "invoicing", "to priced", "completed"]
        if not job:
            return render_json(None, 404)

        try:
            data = request.json
            if not data.get('status', None):
                raise Exception("You must specific a status when editing a job.")

            for s in valid_statuses:
                if s == data['status']:
                    job.status = s
                    session.commit()
                    return render_json(None, 204)

            raise Exception(f"Invalid status {data['status']}, must be one of {','.join(valid_statuses)}")

        except Exception as e:
            return render_json({'message': f"Invalid payload: {e}"}, 400)


@app.route('/job/<string:job_id>/note', methods=['POST'])
def add_job_note(job_id):
    with Db() as session:
        job = Query(Jobs).with_session(session).filter(Jobs.job_id == job_id).first()

        if not job:
            return render_json({'message': f'Unknown job_id {job_id}'}, 404)

        try:
            data = request.json
            if not data.get('data', None):
                raise Exception("Check payload, data key is mandatory.")

        except Exception as e:
            return render_json({'message': f"Invalid payload: {e}"})

        note_id = str(uuid.uuid4())
        note = Notes(
            note_id=note_id,
            job_id=job_id,
            data=data.get('data')
        )
        session.add(note)
        session.commit()
        return render_json({'note_id': note_id})


@app.route('/note/<string:note_id>', methods=['PATCH'])
def update_job_note(note_id):
    with Db() as session:
        note = Query(Notes).with_session(session).filter(Notes.note_id == note_id).first()

        if not note:
            return render_json({'message': f'Unknown note_id {note_id}'}, 404)

        try:
            data = request.json
            if not data.get('data', None):
                raise Exception("Check payload, data key is mandatory.")

        except Exception as e:
            return render_json({'message': f"Invalid payload: {e}"})

        note.data = data['data']
        session.commit()
        return render_json(None, 204)


if __name__ == "__main__":
    logger.info("Booting app on %s..." % _app_config.get("port"))
    app.run(host=_app_config.get("host"),
            port=_app_config.get("port"),
            debug=True)
git