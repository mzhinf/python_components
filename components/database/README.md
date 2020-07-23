##### How to create test environment
[mysql](https://hub.docker.com/_/mysql)

```
# Pull MySQL images
docker pull mysql:5.7
# Create MySQL container
docker run --name mysql-test -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
# Connect to MySQL and create database
docker exec -it mysql-test /bin/bash
mysql -u root -p123456
CREATE DATABASE component;
```

##### How to test this component
- Fill in MySQL information to test/database/test_sql_utils.py
```
CONFIG = {
    'uri': {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'database': 'component',
        'host': 'localhost',
        'port': 3307,
        'username': 'root',
        'password': '123456'
    },
    'echo': True  # log all sql statements
}
```
