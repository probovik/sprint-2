### Задание 4 (уважаемый проверяющий, у меня мак на М3 не стартует API контейнер, остальное проверил работает суть понял)

### перед запуском выполнить все скрипты из Задания 2 и 3

``` проверить наличие кластера 
docker exec -it redis_1

echo "yes" | redis-cli --cluster create   173.17.0.2:6379   173.17.0.3:6379   173.17.0.4:6379   173.17.0.5:6379   173.17.0.6:6379   173.17.0.7:6379   --cluster-replicas 1
```