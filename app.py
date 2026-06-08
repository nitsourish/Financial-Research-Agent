import uuid
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from main import main
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
jobs = {}
class RequestObject(BaseModel):
    ticker: str
    
@app.post("/research")
async def create_research(request: RequestObject, back_ground_task:BackgroundTasks):
   job_id = str(uuid.uuid4()) 
   jobs[job_id] = {"status": "running", "ticker": request.ticker, 'result':None}
   
   def run(ticker, job_id):
       jobs[job_id]["result"] = main(ticker)
       jobs[job_id]["status"] = "completed"
   back_ground_task.add_task(run, request.ticker, job_id)
   return {"job_id": job_id, "status": "running"}

@app.get("/research/{job_id}")
async def get_result(job_id:str):
    job = jobs.get(job_id)
    if not job:
        return {'error':"job not found"}
    return job
    

@app.get("/health")
async def get_health():
    return {"status": 'healthy'}
