from fastapi import FastAPI
import psycopg2
import traceback
from dotenv import dotenv_values
from pydantic import BaseModel
# Сущности:
# 1. Работники
# Имя
# фамилия
# Электронная почта
# номер телефона
# Адрес
# Должность
# зарплата
#  2. Отделы
# Название отдела
# Средняя зарплата
# Количество сотрудников
# В отделе может работать несколько сотрудников, один со-
# трудник может работать только в одном отделе.
# Написать endpoints:
# 1. Вывод всех сотрудников в виде (Имя, должность, телефон)
# 2. Получение полной информации о сотруднике
# 3. Добавление сотрудника
# 4. Удаление сотрудника
# 5. Вывод сотрудников определённого отдела (Имя, Фамилия, Должность)
# 6. Получение информации об отделах (Название, количество сотрудников)
# 7. Добавление отдела
# 9. удаление отдела (если есть сотрудники удаление не возможно)


config = dotenv_values(".env")

connect = psycopg2.connect(
    host=config["HOST"],
    port=config["PORT"],
    database=config["DB_NAME"],
    user=config["USER_ID"],
    password=config["USER_PD"]
)

cursor = connect.cursor()

app = FastAPI()

class vm_workers(BaseModel):
    id: int
    name: str
    position: str
    tel_number : str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/get_workers")
def get_workers():
    try:
        cursor.execute("""
        select name, position, tel_number 
        from workers;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append({
            "name": worker[0],
            "position": worker[1],
            "tel_number":worker[2] })
        return result
    except Exception as e:
        return {"error": traceback.format_exc()}
class vm_get_worker(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    tel_number : str
    address: str
    position: str
    salary: float
    department: str

@app.get("/get_workers_oll_data")
def get_worker_oll_data():
    try:
        cursor.execute("""
        select name, last_name, email, tel_number, adress, position, salary
        from workers;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append({
            "name": worker[0],
            "last_name": worker[1],
            "email":worker[2],
            "tel_number":worker[3],
            "adress":worker[4],
            "position":worker[5],
            "salary":worker[6]})
        return result
    except Exception as e:
        return {"error": traceback.format_exc()}
class vm_get_workers_oll_data(BaseModel):
    name: str
    last_name: str
    email: str
    tel_number : str
    address: str
    position: str
    salary: float

@app.post("/add_worker")
def add_worker(worker: vm_get_worker):
    name = worker.name['name']
    last_name = worker.surname['last_name']
    email = worker.email['email']
    tel_number = worker.tel_number['tel_number']
    adress = worker.address['adress']
    position = worker.position['position']
    salary = worker.salary['salary']
    department = worker.department['department']
    cursor.execute("""
    insert into workers (name, last_name, email, tel_number, adress, position, salary, department)
    values (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (name, last_name, email, tel_number, adress, position, salary, department))
    connect.commit()
    return {"message": f'Сотрудник {name},{last_name},{email},{tel_number},{adress},{position},{salary},{department} добавлен'}

@app.delete("/delete_worker")
def delete_worker(worker: vm_get_worker):
    name = worker.name['name']
    last_name = worker.surname['last_name']
    email = worker.email['email']
    tel_number = worker.tel_number['tel_number']
    adress = worker.address['adress']
    position = worker.position['position']
    salary = worker.salary['salary']
    department = worker.department['department']
    cursor.execute("""
    delete from workers where name = %s and last_name = %s and email = %s and tel_number = %s and adress = %s and position = %s and salary = %s and department = %s;
    """, (name, last_name, email, tel_number, adress, position, salary, department))
    connect.commit()
    return {"message": f'Сотрудник {name},{last_name},{email},{tel_number},{adress},{position},{salary},{department} удален'}

@app.get("/get_workers_department")
def get_workers_department():
    try:
        cursor.execute("""
        select name, count(name)
        from workers
        group by name;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append({
            "name": worker[0],
            "count": worker[1]})
        return result
    except Exception as e:
        return {"error": traceback.format_exc()}

@app.post("/add_department")
def add_department(department: vm_get_workers_oll_data):
    name = department.name['name']
    count = department.count['count']
    cursor.execute("""
    insert into department (name, count)
    values (%s, %s);
    """, (name, count))
    connect.commit()
    return {"message": f'Отдел {name},{count} добавлен'}

@app.delete("/delete_department")
def delete_department(department: vm_get_workers_oll_data):
    name = department.name['name']
    count = department.count['count']
    cursor.execute("""
    delete from department where name = %s and count = %s;
    """, (name, count))
    connect.commit()
    return {"message": f'Отдел {name},{count} удален'}

