# Password Manager

A menu-driven command-line password manager implemented in Python. It stores user accounts and website credentials in a MySQL database, and uses Fernet encryption from the `cryptography` package for password-related values. The runnable program is [Python Password Manager.py](<./Python Password Manager.py>).

> **Security notice:** This is an educational prototype demonstrating password management, database integration, and symmetric encryption. It has known security limitations and is not intended for storing real-world credentials or production use.

## Features

- Sign up and log in with an application user name and password.
- Add, display, delete, and change website credentials.
- Validate website passwords against the specified length and character requirements: 8–16 characters, lowercase and uppercase letters, a digit, a character from `_$#@`, and no whitespace.
- Offer a randomly generated password suggestion when an entered website password fails validation.
- Temporarily lock an account for 30 minutes after three failed login attempts.
- Create the MySQL database and tables when the program reaches its main menu.

## Technology

| Component | Use |
| --- | --- |
| Python standard library | Console input/output, file handling, serialization, random selection, regular expressions, and time calculations |
| `cryptography` | Fernet encryption and decryption |
| `mysql-connector-python` | Connection to MySQL and database operations |
| `tabulate` | Displaying saved website credentials in a table |
| MySQL | Persistent storage for application accounts and website credentials |

## Requirements

- Python 3 and `pip`.
- A running MySQL server reachable at `localhost`.
- A MySQL account that can create and use the `Password_Manager` database and its tables.

Before running the program, set the MySQL connection values in the Python script to match your local server.

## Installation and running

From the repository root, install the third-party packages used by the script:

```shell
python -m pip install cryptography mysql-connector-python tabulate
```

Start the MySQL server, configure the connection settings in the script as needed, then run:

```shell
python "Python Password Manager.py"
```

The program connects to MySQL at startup. Follow the prompts to create the initial master password, then choose an option from the sign-up/login/exit menu. After the menu choice, the program creates the `Password_Manager` database and its `Master` and `Passwords` tables if they do not already exist. Once logged in, the account menu provides options to add, display, delete, or change credentials and to log out.

Run the program from a directory where it can create and access its local data files. Relative file paths are resolved from the current working directory.

## Data and files

- MySQL database `Password_Manager` holds application account records in `Master` and website credentials in `Passwords`.
- `secret.key` is generated in the current working directory when encryption is first used. It is required to decrypt values encrypted with that key.
- `masterpassword.dat` stores the serialized encrypted master-password value using Python's pickle mechanism.
- `temp.dat` is used temporarily when changing the master password.

Back up `secret.key` securely and independently from the database. Losing the key prevents decryption of values encrypted with it.

## Repository structure

```text
.
├── Python Password Manager.py
└── README.md
```

- [Python Password Manager.py](<./Python Password Manager.py>) — the runnable application.
- `README.md` — project documentation.

## Security considerations

The implementation has security limitations:

- The encryption key is stored as a local file alongside the program's other local data, rather than in a separate protected key store.
- The Fernet key is kept in `secret.key`, while encrypted values are stored in MySQL and the master-password value is stored in `masterpassword.dat`. Anyone obtaining the key and corresponding encrypted values may be able to decrypt them.
- `masterpassword.dat` is loaded using Python's `pickle` mechanism. Only load this file from a trusted source; untrusted pickle files can execute code during deserialization.
- The database account needs permission to create and use the application's database; use a dedicated account with only the required privileges.
- Some SQL statements concatenate user input into query strings instead of using parameterized queries.
- The master-password check assigns `c` inside the function without updating the module-level `c` used by the main loop. As a result, entering an incorrect master password does not trigger the main loop's rejection branch, and the menu can still be reached.
- When a website password fails validation, declining the generated suggestion returns the original input, which the add flow still stores.
- The password generator uses Python's `random` module rather than `secrets`, which is designed for cryptographically secure random generation.
- Password and master-password prompts use ordinary console input; entered text is not masked.
- Sign-up collects a security question and answer, but neither is used in the login flow.

