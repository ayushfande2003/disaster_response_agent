from datetime import datetime
from typing import Optional

class DisasterReport:
    def __init__(self, id: int, title: str, description: str, 
                 location: str, severity: str, reporter_name: str,
                 file_path: Optional[str] = None, 
                 created_at: Optional[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.location = location
        self.severity = severity
        self.reporter_name = reporter_name
        self.file_path = file_path
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "severity": self.severity,
            "reporter_name": self.reporter_name,
            "file_path": self.file_path,
            "created_at": self.created_at
        }
