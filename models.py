# app/models.py  

from pydantic import BaseModel  
from typing import Optional  
from datetime import datetime  

class TestReport(BaseModel):  
    id: Optional[str]  # MongoDB ObjectId will be converted to string  
    projectName: str  
    authors: Optional[str] = ""  
    storyTests: int  
    regressionTestsAutomated: int  
    regressionTestsManual: int  
    totalTestsByApplication: int  

    # Story Test Results  
    storyPassed: int  
    storyFailed: int  
    storyUnexecuted: int  
    storyBlocked: int  
    storySkipped: int  
    storyCritical: int  
    storyNew: int  
    storyUnused: int  
    storyBugs: int  

    # Automation Test Results (AR)  
    arPassed: int  
    arFailed: int  
    arUnexecuted: int  
    arBlocked: int  
    arSkipped: int  
    arCritical: int  
    arNew: int  
    arUnused: int  
    arBugs: int  

    # Manual Regression Test Results (MR)  
    mrPassed: int  
    mrFailed: int  
    mrUnexecuted: int  
    mrBlocked: int  
    mrSkipped: int  
    mrCritical: int  
    mrNew: int  
    mrUnused: int  
    mrBugs: int  

    createdAt: Optional[datetime] = None