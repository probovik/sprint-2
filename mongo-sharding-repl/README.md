### Задание 3 (уважаемый проверяющий, у меня мак на М3 не стартует API контейнер, остальное проверил работает суть понял)

### перед запуском выполнить все скрипты из Задания 2

``` подключаемся к первому шарду и инициализируем реплики
 docker exec -it shard1-1 mongosh --port 27018

rs.initiate({_id: "shard1-1", members: [ {_id: 0, host: "shard1-1:27018"}, {_id: 1, host: "shard1-1replica1:27028"},{_id: 2, host: "shard1-1replica2:27038"}, {_id: 3, host: "shard1-1replica3:27048"}]})
exit();

docker exec -it shard1-2 mongosh --port 27019

rs.initiate({_id: "shard1-2replica", members: [ {_id: 0, host: "shard1-2:27019"}, {_id: 1, host: "shard1-2secondary1:27029"}, {_id: 2, host: "shard1-2secondary2:27039"}, {_id: 3, host: "shard1-2secondary3:27049"}]})

exit();

``` 