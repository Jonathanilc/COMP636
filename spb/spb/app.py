from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from db import db_functions
from services import db_service

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/currentjobs")

@app.route("/currentjobs")
def currentjobs():
    jobList = db_service.getJobs()
    return render_template("currentjoblist.html", job_list = jobList)    

@app.route("/admin")
def admin():
    return render_template("admin.html")   

@app.route("/admin/customers")
def customers():
    return render_template(
        "customers.html",
        customers = db_functions.getCustomers()
    )

@app.route("/admin/services")
def services():
    return render_template("services.html")

@app.route("/admin/parts")
def parts():
    return render_template("parts.html")

@app.route("/admin/schedulejob")
def scheduleJob():
    return render_template("schedule_job.html")

@app.route("/admin/unpaidbills")
def unpaidBills():
    return render_template("unpaid_bills.html")

@app.route("/admin/overduebills")
def overdueBills():
    return render_template("overdue_bills.html")

@app.route("/jobs/<int:jobId>")
def job(jobId = None):
    
    return render_template(
        "job.html",
        job = db_service.getSingleJob(job_id=jobId),
        existingServices = db_functions.getServicesByJobId(job_id=jobId),
        services = db_functions.getAllServices(),
        existingParts = db_functions.getPartsByJobId(job_id=jobId),
        parts = db_functions.getAllParts(),
        jobId = jobId
    )


# POST ROUTE

@app.route("/jobs/<int:jobId>/addservice", methods=["POST"])
def addService(jobId = None):
    serviceId = request.form.get('service')
    qty = request.form.get('quantity')
    db_service.addService(job_id=jobId, service_id=serviceId, qty=qty)
    return redirect(f"/jobs/{jobId}")

@app.route("/jobs/<int:jobId>/changeserviceqty", methods=["POST"])
def changeServiceQty(jobId = None):
    serviceId = request.form.get('service')
    qty = request.form.get('quantity')
    db_service.changeServiceQty(job_id=jobId, service_id=serviceId, qty=qty)
    return redirect(f"/jobs/{jobId}")

@app.route("/jobs/<int:jobId>/deleteservice", methods=["POST"])
def deleteService(jobId = None):
    serviceId = request.form.get('service')
    db_functions.deleteService(job_id=jobId, service_id=serviceId)
    return redirect(f"/jobs/{jobId}")


@app.route("/jobs/<int:jobId>/addpart", methods=["POST"])
def addPart(jobId = None):
    partId = request.form.get('part')
    qty = request.form.get('quantity')
    db_service.addPart(job_id=jobId, part_id=partId, qty=qty)
    return redirect(f"/jobs/{jobId}")


@app.route("/jobs/<int:jobId>/changepartqty", methods=["POST"])
def changePartQty(jobId = None):
    partId = request.form.get('part')
    qty = request.form.get('quantity')
    db_service.changePartQty(job_id=jobId, part_id=partId, qty=qty)
    return redirect(f"/jobs/{jobId}")

@app.route("/jobs/<int:jobId>/deletepart", methods=["POST"])
def deletePart(jobId = None):
    partId = request.form.get('part')
    db_functions.deletePart(job_id=jobId, part_id=partId)
    return redirect(f"/jobs/{jobId}")

@app.route("/jobs/<int:jobId>/complete", methods=["POST"])
def completeJob(jobId = None):
    db_service.completeJob(job_id=jobId)
    return redirect(f"/jobs/{jobId}")

@app.route("/jobs/<int:jobId>/restore", methods=["POST"])
def restoreJob(jobId = None):
    db_functions.restoreJob(job_id=jobId)
    return redirect(f"/jobs/{jobId}")