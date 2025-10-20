import sqlite3
import json
from typing import List, Optional
from models import DisasterReport

class Database:
    def __init__(self, db_path: str = "data/disaster_reports.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                severity TEXT NOT NULL,
                reporter_name TEXT NOT NULL,
                file_path TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_report(self, report: DisasterReport) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reports (title, description, location, severity, 
                               reporter_name, file_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (report.title, report.description, report.location, 
              report.severity, report.reporter_name, report.file_path, 
              report.created_at))
        conn.commit()
        report_id = cursor.lastrowid
        conn.close()
        print(f"[ALERT] New disaster report submitted: {report.title} at {report.location} (Severity: {report.severity})")
        return report_id
    
    def get_all_reports(self) -> List[dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "location": row[3],
                "severity": row[4],
                "reporter_name": row[5],
                "file_path": row[6],
                "created_at": row[7]
            })
        return reports
    
    def get_report_by_id(self, report_id: int) -> Optional[dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "location": row[3],
                "severity": row[4],
                "reporter_name": row[5],
                "file_path": row[6],
                "created_at": row[7]
            }
        return None
    
    def get_alerts(self) -> List[dict]:
        """Get high severity reports as alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reports 
            WHERE severity IN ('Critical', 'High')
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        alerts = []
        for row in rows:
            alerts.append({
                "id": row[0],
                "title": row[1],
                "location": row[3],
                "severity": row[4],
                "created_at": row[7]
            })
        return alerts
