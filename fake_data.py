from faker import Faker
import csv
import random

fake = Faker()

data = []

for _ in range(100):
    name = fake.name()
    email = fake.email()
    address = fake.address()
    country = fake.country()
    dob = fake.date_of_birth()
    company = fake.company()
    job = fake.job()
    age = fake.random_int(min=18, max=99)
    revenue = random.uniform(1000, 10000)
    data.append([name, email, age,address,country,dob,company,job,age,revenue])
    
csv_file = "fake_data.csv"

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Address", "Country","dob", "Country", "Job", "Age", "Revenue"])

    for row in data:
        writer.writerow(row)