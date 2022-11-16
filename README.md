# REST API with web client
* not a stable version (under maintenance)
- API : Fast API with sqlite database
- WEB : Vue JS

## serving setup
### api
1. masuk direktori api
2. install dependensi ```pip install -r requirements.txt ```
1. serving api ```uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload```
   
### web client
1. masuk ke direktori web, install semua dependensi ```npm install```
2. masuk ke direktori web, install semua dependensi```npm run serve```



## deploying with docker
1. pastiin udah di direktori root project
2. eksekusi build local web ```./build-web-local.sh```, kalau belum executable ```chmod u+x build-web-local.sh```
3. eksekusi docker composenya ```docker-compose up -d```