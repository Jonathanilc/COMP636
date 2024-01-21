from db import db_functions

def _add(job_id, id, qty, type):
    if int(qty) <= 0:
        return
    count = 0
    exiting = db_functions.getServicesByJobIdAndServiceId(job_id=job_id,service_id=id) if type == "service" else db_functions.getPartsByJobIdAndPartId(job_id=job_id,part_id=id)
    for service in exiting:
        count += int(service[3])
    if count > 0:
        db_functions.deleteService(job_id=job_id, service_id=id) if type == "service" else db_functions.deletePart(job_id=job_id, part_id=id)
        db_functions.addService(job_id=job_id, service_id=id, qty=int(qty) + int(count)) if type == "service" else db_functions.addPart(job_id=job_id, part_id=id, qty=int(qty) + int(count))
        return
    db_functions.addService(job_id=job_id,service_id=id, qty=qty) if type == "service" else db_functions.addPart(job_id=job_id,part_id=id, qty=qty)
    
def _changeQty(job_id, id, qty, type):
    if qty == 0:
        db_functions.deleteService(job_id=job_id, service_id=id) if type == "service" else db_functions.deletePart(job_id=job_id, part_id=id)
        return
    db_functions.deleteService(job_id=job_id, service_id=id) if type == "service" else db_functions.deletePart(job_id=job_id, part_id=id)
    db_functions.addService(job_id=job_id, service_id=id, qty=int(qty)) if type == "service" else db_functions.addPart(job_id=job_id, part_id=id, qty=int(qty))

    

def getJobs():
    jobList = db_functions.getJobsWithCustomerName()
    # merge the first name and the family name.
    result = [(item[0], f"{item[1]} {item[2]}", item[3]) for item in jobList]
    return result

def getSingleJob(job_id):
    job = db_functions.getSingleJob(job_id=job_id);
    result = [(f"{item[0]} {item[1]}", item[2], item[3], f"{'Yes' if item[4] == 1 else 'No' }", f"{'Yes' if item[5] == 1 else 'No' }") for item in job]
    return result


def addService(job_id, service_id, qty):
    return _add(job_id=job_id, id=service_id, qty=qty, type="service")

    
def addPart(job_id, part_id, qty):
    return _add(job_id=job_id, id=part_id, qty=qty, type="part")

def changeServiceQty(job_id, service_id, qty):
    return _changeQty(job_id=job_id, id=service_id, qty=qty, type="service")
    
def changePartQty(job_id, part_id, qty):
    return _changeQty(job_id=job_id, id=part_id, qty=qty, type="part")


def completeJob(job_id):
    services = db_functions.getServicesByJobId(job_id=job_id)
    parts = db_functions.getPartsByJobId(job_id=job_id)
    totalCost =  sum(float(cost) * int(qty) for _, cost, qty, *_ in services) + sum(float(cost) * int(qty) for _, cost, qty, *_ in parts)
    return db_functions.completeJob(job_id=job_id, total_cost=totalCost)