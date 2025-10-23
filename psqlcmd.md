Excellent — you want a **PostgreSQL interactive-mode cheat sheet** 💪
Here’s a clean reference of all the important commands **to manage users, databases, and tables directly inside `psql`** (the interactive terminal).

---

## 🧭 **Basic Navigation in `psql`**

All commands starting with a backslash `\` are **meta-commands** specific to PostgreSQL.

| Action                    | Command                | Example              |
| ------------------------- | ---------------------- | -------------------- |
| **List all databases**    | `\l` **or** `\list`    |                      |
| **Connect to a database** | `\c dbname [username]` | `\c shopdb shopuser` |
| **Show current database** | `\conninfo`            |                      |
| **List all users/roles**  | `\du`                  |                      |
| **Exit psql**             | `\q`                   |                      |

---

## 🏗️ **Database Management**

| Action                         | SQL Command               | Example                   |
| ------------------------------ | ------------------------- | ------------------------- |
| **Create a new database**      | `CREATE DATABASE dbname;` | `CREATE DATABASE shopdb;` |
| **Delete (drop) a database**   | `DROP DATABASE dbname;`   | `DROP DATABASE shopdb;`   |
| **Show all databases**         | `\l`                      |                           |
| **Switch to another database** | `\c dbname`               | `\c shopdb`               |

---

## 👥 **User / Role Management**

| Action                                       | SQL Command                                                        | Example                                                |
| -------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ |
| **Create user**                              | `CREATE USER username WITH PASSWORD 'password';`                   | `CREATE USER shopuser WITH PASSWORD 'mypassword';`     |
| **Grant privileges on database**             | `GRANT ALL PRIVILEGES ON DATABASE dbname TO username;`             | `GRANT ALL PRIVILEGES ON DATABASE shopdb TO shopuser;` |
| **Grant privileges on all tables in schema** | `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;` |                                                        |
| **Revoke privileges**                        | `REVOKE ALL PRIVILEGES ON DATABASE dbname FROM username;`          |                                                        |
| **Drop user**                                | `DROP USER username;`                                              | `DROP USER shopuser;`                                  |
| **List all users**                           | `\du`                                                              |                                                        |

---

## 🧱 **Tables Management**

| Action                            | SQL Command | Example |
| --------------------------------- | ----------- | ------- |
| **List all tables in current DB** | `\dt`       |         |
| **Create a table**                |             |         |
|                                   | ```sql      |         |
| CREATE TABLE products (           |             |         |

```
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
name VARCHAR(100),
price NUMERIC(10,2),
category VARCHAR(50)
```

);

````| |
| **Insert data** |  |
| | `INSERT INTO products (name, price, category) VALUES ('Olive Oil', 100.00, 'Natural Oil');` |  |
| **View table data** | `SELECT * FROM products;` |  |
| **View table with filters** | `SELECT name, price FROM products WHERE category = 'Natural Oil';` |  |
| **List columns of a table** | `\d tablename` | `\d products` |
| **Drop a table** | `DROP TABLE tablename;` | `DROP TABLE products;` |

---

## 🔐 **Granting Permissions Examples**

Grant all rights for one user on one table:
```sql
GRANT ALL PRIVILEGES ON TABLE products TO shopuser;
````

Grant select/insert only:

```sql
GRANT SELECT, INSERT ON TABLE products TO shopuser;
```

---

## 🧹 **Dropping Things Safely**

| Drop Type     | Command                 | Example                 |
| ------------- | ----------------------- | ----------------------- |
| Drop user     | `DROP USER username;`   | `DROP USER shopuser;`   |
| Drop database | `DROP DATABASE dbname;` | `DROP DATABASE shopdb;` |
| Drop table    | `DROP TABLE tablename;` | `DROP TABLE products;`  |

---

## 🧠 **Useful Extras**

| Action                       | Command                | Example       |
| ---------------------------- | ---------------------- | ------------- |
| Show current user            | `SELECT current_user;` |               |
| Show all schemas             | `\dn`                  |               |
| Show all functions           | `\df`                  |               |
| Describe a table (structure) | `\d tablename`         | `\d products` |

---

Would you like me to make a **ready `.sql` file** containing example commands (create DB, user, grant privileges, create table, insert, select, drop etc.) so you can just run it and test everything?
Excellent 🔥 — here’s a **complete reference** of all `psql` connection methods and parameters for accessing PostgreSQL with a user.

---

## 🧩 1️⃣ Basic `psql` Syntax

```bash
psql [OPTIONS] [DBNAME [USERNAME]]
```

Or using flags (recommended):

```bash
psql -U <user> -d <database> -h <host> -p <port>
```

---

## 🧠 2️⃣ Common Parameters (Flags)

| Flag     | Meaning                      | Example                          |
| -------- | ---------------------------- | -------------------------------- |
| `-U`     | Username                     | `-U pro-eng`                     |
| `-d`     | Database name                | `-d pro_eng`                     |
| `-h`     | Host (server)                | `-h localhost` or `-h 127.0.0.1` |
| `-p`     | Port (default 5432)          | `-p 5432`                        |
| `-W`     | Force password prompt        | `-W`                             |
| `-w`     | Never prompt for password    | `-w`                             |
| `-c`     | Execute a single SQL command | `-c "SELECT version();"`         |
| `-f`     | Execute commands from a file | `-f script.sql`                  |
| `-l`     | List all databases           | `psql -l`                        |
| `-v`     | Set psql variable            | `-v var=value`                   |
| `--help` | Show help info               | `psql --help`                    |

---

## 🧱 3️⃣ Connection Examples

### 🟢 Local socket (peer auth)

No password, connects via local UNIX socket:

```bash
psql -U pro-eng -d pro_eng
```

*(works only if Linux user = PostgreSQL user and `peer` auth enabled)*

---

### 🟡 TCP connection with password (localhost)

```bash
psql -U pro-eng -h localhost -d pro_eng -W
```

If PostgreSQL listens on another port:

```bash
psql -U pro-eng -h localhost -p 5433 -d pro_eng -W
```

---

### 🟣 Remote connection

```bash
psql -U pro-eng -h 192.168.1.10 -p 5432 -d pro_eng -W
```

---

### 🔵 Connect as superuser

```bash
sudo -u postgres psql
```

Or explicitly:

```bash
psql -U postgres -h localhost -d postgres -W
```

---

### 🟤 Connect to a database interactively

If you’re already inside `psql`, you can switch databases:

```sql
\c database_name user_name
```

Example:

```sql
\c pro_eng pro-eng
```

---

### ⚪ List, inspect, and exit

Once inside psql:

| Command     | Description          |
| ----------- | -------------------- |
| `\l`        | List databases       |
| `\du`       | List roles/users     |
| `\dn`       | List schemas         |
| `\dt`       | List tables          |
| `\conninfo` | Show connection info |
| `\q`        | Quit psql            |

---

## 🧾 4️⃣ Full Examples

#### Example 1 – Standard password login

```bash
psql -U pro-eng -h localhost -d pro_eng -W
```

#### Example 2 – Run one command directly

```bash
psql -U pro-eng -h localhost -d pro_eng -c "SELECT NOW();"
```

#### Example 3 – Run SQL from file

```bash
psql -U pro-eng -h localhost -d pro_eng -f ./init.sql
```

#### Example 4 – List all available databases

```bash
psql -U postgres -l
```

---

## ⚙️ 5️⃣ Environment Variables (Optional)

Instead of flags, you can set env vars:

```bash
export PGUSER=pro-eng
export PGPASSWORD=your_password
export PGDATABASE=pro_eng
export PGHOST=localhost
export PGPORT=5432
```

Then simply run:

```bash
psql
```

---

Would you like me to show **all the psql flags** (full official list from `psql --help`) or just keep this as your practical daily reference?
