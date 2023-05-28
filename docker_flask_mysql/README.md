# Docker Flask MySQL Project

This project utilizes Docker to containerize a simple Flask application and a MySQL database. The Flask application provides a web form to collect user information (name and email) and stores it in the MySQL database.
該項目利用 Docker 將一個簡單的 Flask 應用程序和一個 MySQL 數據庫容器化。 Flask 應用程序提供了一個 Web 表單來收集用戶信息（姓名和電子郵件）並將其存儲在 MySQL 數據庫中。

## Project Structure
```.
├── README.md
├── docker-compose.yaml
├── flask
│   ├── Dockerfile
│   └── flask_app
│       ├── app.py
│       ├── requirements.txt
│       └── tmpfolder
│           ├── index.html
│           └── success.html
└── mysql
    ├── Dockerfile
    └── init.sql
```

## Prerequisites
Make sure that you have Docker installed on your system. If not, follow the official Docker documentation to install them.

## Setting Up Environment Variables
* Create a new file in your project root directory named `.env`.
  
```.env
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=shop
```

## Building and Running the Application
Navigate to the root directory of the project in the terminal and execute the following command:

```bash
docker-compose up -d --build
```

## Accessing the Application
Once the application is running, navigate to http://localhost:8001 in your web browser. You should see a web form where you can enter a name and an email. On submission, these details are stored in the MySQL database.
應用程序運行後，在 Web 瀏覽器中導航至 http://localhost:8001 。您應該會看到一個 Web 表單，您可以在其中輸入姓名和電子郵件。提交時，這些詳細信息存儲在 MySQL 數據庫中。

## Inspecting Data in the MySQL Database
To check the data that's been stored in the MySQL database, you'll need to access the MySQL shell inside the running MySQL container:
要檢查存儲在 MySQL 數據庫中的數據，您需要訪問正在運行的 MySQL 容器內的 MySQL shell：
```bash
docker-compose exec mysql sh -c 'mysql -uroot -p${MYSQL_ROOT_PASSWORD}'
```
This will open a MySQL shell where you can issue SQL commands. To select the database you specified in your .env file and inspect the users table, use the following commands:
這將打開一個 MySQL shell，您可以在其中發出 SQL 命令。要選擇您在 .env 文件中指定的數據庫並檢查 users 表，請使用以下命令：

```mysql
USE shop;
SELECT * FROM users;
```

## Architecture
The application consists of two main parts:
1. **Flask Application**: This is a simple web application built with Flask. It provides a form for users to enter their name and email, which is then stored in a MySQL database.

2. **MySQL Database**: This is a MySQL database that stores the user data inputted via the Flask application.

Docker Compose orchestrates these two services. The `docker-compose.yaml` file defines the services, their configurations, and the relationships between them. Notably, the Flask service is marked as dependent on the MySQL service through the `depends_on` key. This ensures the database is ready before the application starts.
Docker Compose 協調這兩個服務。 docker-compose.yaml 文件定義服務、它們的配置以及它們之間的關係。值得注意的是，Flask 服務通過 depends_on 鍵被標記為依賴於 MySQL 服務。這確保數據庫在應用程序啟動之前就緒。

## MySQL Initialization
In the MySQL directory, there is a `Dockerfile` for creating the MySQL Docker image and an `init.sql` file for initializing the database.

The `init.sql` file is run when the MySQL Docker container is created, and it sets up the initial database structure. Specifically, it creates a table named `users` with columns for id, name, and email.

## Wrapping Up 
This project provides a basic example of how to containerize a Flask application with a MySQL database using Docker. It highlights several important concepts, such as service dependencies, environment variable usage, and database connections. While the application is simple, the principles it demonstrates are applicable to more complex applications.

此專案說明如何使用 Docker 將帶有 MySQL 數據庫的 Flask 應用程序容器化。它強調了幾個重要的概念，例如服務依賴性、環境變量使用和數據庫連接。雖然應用程序很簡單，但它展示的原理適用於更複雜的應用程序。
