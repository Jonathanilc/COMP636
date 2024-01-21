import mysql.connector
from mysql.connector import FieldType

from db import connect

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def query(sql):
    connection = getCursor()
    connection.execute(sql)
    result = connection.fetchall()
    return result


# Job repo
def getJobs():
    return query("""
        SELECT job_id,customer,job_date
        FROM job 
        WHERE completed = 0;
    """)

def getSingleJob(job_id):
    return query(f"""
        SELECT customer.first_name, customer.family_name, job.total_cost, job.job_date, job.completed, job.paid
        FROM job
        LEFT JOIN customer ON job.customer = customer.customer_id
        WHERE job_id = {job_id}
        ORDER BY job_id;
    """)
    
def completeJob(job_id, total_cost):
    return query(f"""
        UPDATE job
        SET completed = 1,total_cost = {total_cost}
        WHERE job.job_id = {job_id};
    """)
    
def restoreJob(job_id):
    return query(f"""
        UPDATE job
        SET completed = 0,total_cost = NULL
        WHERE job.job_id = {job_id};
    """)

def getJobsWithCustomerName():
    return query("""
        SELECT job.job_id, customer.first_name, customer.family_name, job.job_date
        FROM job 
        LEFT JOIN customer ON job.customer = customer.customer_id
        WHERE completed = 0
        ORDER BY job_id;         
    """)

# Customer repo
def getCustomers():
    return query("""
        SELECT * FROM customer
        ORDER BY family_name, first_name;
    """)


# Service repo
def getAllServices():
    return query("SELECT * FROM service")

# JobService repo
def getServicesByJobId(job_id):
    return query(f"""
        SELECT service.service_name, service.cost, job_service.qty, service.service_id
        FROM job_service
        LEFT JOIN service ON job_service.service_id = service.service_id
        WHERE job_service.job_id = {job_id}
        ORDER BY service.service_name ASC;
    """)
    
def getServicesByJobIdAndServiceId(job_id, service_id):
    return query(f"""
        SELECT service.service_id, service.service_name, service.cost, job_service.qty
        FROM job_service
        LEFT JOIN service ON job_service.service_id = service.service_id
        WHERE job_service.job_id = {job_id} AND job_service.service_id = {service_id};
    """)

def addService(job_id, service_id, qty):
    return query(f"""
        INSERT INTO job_service (job_id, service_id, qty)
        VALUES ({job_id}, {service_id}, {qty});
    """)
    
def deleteService(job_id, service_id):
    return query(f"""
        DELETE FROM job_service
        WHERE job_id = {job_id} AND service_id = {service_id} ;
    """)


# Part repo
def getAllParts():
    return query("SELECT * FROM part")

def getPartsByJobId(job_id):
    return query(f"""
        SELECT part.part_name, part.cost, job_part.qty, part.part_id
        FROM job_part
        LEFT JOIN part ON job_part.part_id = part.part_id
        WHERE job_part.job_id = {job_id}
        ORDER BY part.part_name ASC;
    """)

def getPartsByJobIdAndPartId(job_id, part_id):
    return query(f"""
        SELECT part.part_id, part.part_name, part.cost, job_part.qty
        FROM job_part
        LEFT JOIN part ON job_part.part_id = part.part_id
        WHERE job_part.job_id = {job_id} AND job_part.part_id = {part_id};
    """)

# JobPart repo
def addPart(job_id, part_id, qty):
    return query(f"""
        INSERT INTO job_part (job_id, part_id, qty)
        VALUES ({job_id}, {part_id}, {qty});
    """)
    
def deletePart(job_id, part_id):
    return query(f"""
        DELETE FROM job_part
        WHERE job_id = {job_id} AND part_id = {part_id} ;
    """)
    


