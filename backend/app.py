from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import os
from datetime import datetime
from database import Database
from models import DisasterReport

app = FastAPI(title="Disaster Response Agent API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Disaster Response Agent API", "status": "running"}

@app.post("/api/reports")
async def create_report(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    severity: str = Form(...),
    reporter_name: str = Form(...),
    file: UploadFile = File(None)
):
    """Submit a new disaster report"""
    file_path = None
    
    # Handle file upload
    if file and file.filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        file_path = f"uploads/{safe_filename}"
    
    # Create report
    report = DisasterReport(
        id=0,
        title=title,
        description=description,
        location=location,
        severity=severity,
        reporter_name=reporter_name,
        file_path=file_path
    )
    
    report_id = db.add_report(report)
    report.id = report_id
    
    return JSONResponse(
        content={
            "message": "Report submitted successfully",
            "report_id": report_id,
            "data": report.to_dict()
        },
        status_code=201
    )

@app.get("/api/reports")
def get_all_reports():
    """Get all disaster reports"""
    reports = db.get_all_reports()
    return {
        "count": len(reports),
        "reports": reports
    }

@app.get("/api/reports/{report_id}")
def get_report(report_id: int):
    """Get a specific disaster report"""
    report = db.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.get("/api/alerts")
def get_alerts():
    """Get high-priority alerts"""
    alerts = db.get_alerts()
    return {
        "count": len(alerts),
        "alerts": alerts
    }

@app.get("/api/uploads/{filename}")
def get_uploaded_file(filename: str):
    """Serve uploaded files"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@app.get("/api/stats")
def get_statistics():
    """Get statistics about disaster reports"""
    reports = db.get_all_reports()
    
    severity_counts = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }
    
    for report in reports:
        severity = report.get("severity", "Low")
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    return {
        "total_reports": len(reports),
        "severity_breakdown": severity_counts
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
