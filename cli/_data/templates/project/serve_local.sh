pip install -r ./requirements.txt --quiet --no-cache-dir
python ./scripts/maintenance/migrations.py
python ./scripts/maintenance/seeds.py
flask run -h 0.0.0.0 -p 4000