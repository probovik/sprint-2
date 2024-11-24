### Задание 2

Запускаем mongodb и приложение

```shell
docker compose up -d
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

```инициализируйте шарды выполнив поочередно команды
docker exec -it shard1-1 mongosh --port 27018

rs.initiate(
    {
      _id : "shard1-1",
      members: [
        { _id : 0, host : "shard1-1:27018" },
      ]
    }
);

exit();

docker exec -it shard1-2 mongosh --port 27019

rs.initiate(
    {
      _id : "shard1-2replica",
      members: [
        { _id : 1, host : "shard1-2:27019" }
      ]
    }
  );

exit();
```
 
```инициализируйте роутер и наполните его данными выполнив поочередно команды должно получиться 1000 записей
docker exec -it mongos_router mongosh --port 27020

sh.addShard( "shard1-1/shard1-1:27018");
sh.addShard( "shard1-2/shard1-2:27019");

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

``` сделайте проверку на первом шарде получится 492 документа
 docker exec -it shard1-1 mongosh --port 27018
 use somedb;
 db.helloDoc.countDocuments();
 exit();
``` 

``` сделайте проверку на втором шарде получится 508 документов
docker exec -it shard1-2 mongosh --port 27019
use somedb;
db.helloDoc.countDocuments();
exit();
```
