### Задание 4

### 

заменить файл app.py в директории api_app на файл находящийся в этой папке для работы с редис кластером

```shell
docker compose up -d
```

``` проверить наличие кластера 
docker exec -it redis_1 bash

echo "yes" | redis-cli --cluster create   173.17.0.2:6379   173.17.0.3:6379   173.17.0.4:6379   173.17.0.5:6379   173.17.0.6:6379   173.17.0.17:6379   --cluster-replicas 1

exit
```

```инициализируйте сервер конфигурации выполнив поочередно команды
docker exec -it configSrv mongosh --port 27017

rs.initiate(
  {
    _id : "config_server",
       configsvr: true,
    members: [
      { _id : 0, host : "configSrv:27017" }
    ]
  }
);

exit();
```

``` подключаемся к первому шарду и второму шарду инициализируем их и реплики
 docker exec -it shard1-1 mongosh --port 27018

rs.initiate({_id: "shard1-1", members: [ {_id: 0, host: "shard1-1:27018"}, {_id: 1, host: "shard1-1replica1:27028"},{_id: 2, host: "shard1-1replica2:27038"}, {_id: 3, host: "shard1-1replica3:27048"}]})

exit();

docker exec -it shard1-2 mongosh --port 27019

rs.initiate({_id: "shard1-2replica", members: [ {_id: 0, host: "shard1-2:27019"}, {_id: 1, host: "shard1-2secondary1:27029"}, {_id: 2, host: "shard1-2secondary2:27039"}, {_id: 3, host: "shard1-2secondary3:27049"}]})

exit();
``` 

```инициализируйте роутер и наполните его данными выполнив поочередно команды должно получиться 1000 записей

docker exec -it mongos_router mongosh --port 27020

sh.addShard( "shard1-1/shard1-1:27018");
sh.addShard( "shard1-2replica/shard1-2:27019");

sh.enableSharding("somedb");
sh.shardCollection("somedb.helloDoc", { "name" : "hashed" } )

use somedb

var docs = [];
for(var i = 0; i < 1000; i++) {
    docs.push({age:i, name:"ly"+i});
}
db.helloDoc.insertMany(docs);

db.helloDoc.countDocuments() 
exit();
```
