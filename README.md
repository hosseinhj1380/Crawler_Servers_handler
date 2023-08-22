for run server first you need to run this command 
``pip install -r requirements``

to migrate and make database run this command 

`` alembic revision --autogenerate -m "create job model"
alembic upgrade head ``

then run   ``main.py `` file and open ``127.0.0.1:8000/docs/``


you need to have mongodb on your pc and put the correct value on file 
`models/model_explore` to save datas 