```
FV_DOMAIN=localhost
FV_EMAIL=eliot.courtel@wanadoo.fr
FV_API_HOST=0.0.0.0
FV_API_PORT=8080
FV_API_WEBA=*
FV_API_MOD=DEV
FV_API_SCRT=123456
FV_DB_USER=testtest
FV_DB_PASS=testtesttesttest
```

```
docker-compose -f docker-compose.reverse.proxy.yml up -d; \
docker-compose -f docker-compose.filevault.web.yml up -d; \
docker-compose -f docker-compose.filevault.adm.yml up -d;
```
