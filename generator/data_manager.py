#!/usr/bin/env python3
"""
Data Manager Module
Handles all data storage and retrieval operations for the AI Resume Generator
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataManager:
    """Manages user profiles and job application data"""
    
    def __init__(self):
        self.data_dir = "data"
        self.profiles_file = os.path.join(self.data_dir, "user_profiles.json")
        self.applications_file = os.path.join(self.data_dir, "job_applications.json")
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory and files if they don't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"📁 Created data folder: {self.data_dir}")
        
        # Create profiles file if it doesn't exist
        if not os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'w') as f:
                json.dump({}, f)
            print("📝 Created user profiles file")
        
        # Create applications file if it doesn't exist
        if not os.path.exists(self.applications_file):
            with open(self.applications_file, 'w') as f:
                json.dump([], f)
            print("📊 Created job applications file")
    
    def save_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Save user profile data"""
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def load_user_profile(self) -> Optional[Dict[str, Any]]:
        """Load user profile data"""
        try:
            with open(self.profiles_file, 'r') as f:
                data = json.load(f)
                return data if data else None
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def save_job_application(self, application_data: Dict[str, Any]) -> bool:
        """Save a job application record"""
        try:
            applications = self.get_job_applications()
            applications.append(application_data)
            
            with open(self.applications_file, 'w') as f:
                json.dump(applications, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving application: {e}")
            return False
    
    def get_job_applications(self) -> List[Dict[str, Any]]:
        """Get all job applications"""
        try:
            # Check if file exists and is not empty
            if not os.path.exists(self.applications_file):
                print("Applications file doesn't exist, creating new one")
                with open(self.applications_file, 'w') as f:
                    json.dump([], f)
                return []
            
            # Check if file is empty
            if os.path.getsize(self.applications_file) == 0:
                print("Applications file is empty, initializing")
                with open(self.applications_file, 'w') as f:
                    json.dump([], f)
                return []
            
            with open(self.applications_file, 'r') as f:
                data = json.load(f)
                
                # Ensure data is a list
                if not isinstance(data, list):
                    print("Applications file contains invalid data, resetting")
                    data = []
                
                # Clean up corrupted data - ensure all items are dictionaries
                clean_data = []
                for item in data:
                    if isinstance(item, dict):
                        clean_data.append(item)
                    else:
                        print(f"Warning: Skipping corrupted application data: {item}")
                
                # Save cleaned data back if we found corrupted entries
                if len(clean_data) != len(data):
                    print(f"🔧 Cleaned {len(data) - len(clean_data)} corrupted entries")
                    with open(self.applications_file, 'w') as f:
                        json.dump(clean_data, f, indent=2)
                
                return clean_data
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}. Resetting applications file.")
            with open(self.applications_file, 'w') as f:
                json.dump([], f)
            return []
        except Exception as e:
            print(f"Error loading applications: {e}")
            return []
    
    def update_application_status(self, app_index: int, new_status: str) -> bool:
        """Update the status of a specific application"""
        try:
            applications = self.get_job_applications()
            if 0 <= app_index < len(applications):
                applications[app_index]['status'] = new_status
                applications[app_index]['updated_at'] = datetime.now().isoformat()
                
                with open(self.applications_file, 'w') as f:
                    json.dump(applications, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error updating application: {e}")
            return False
    
    def get_application_stats(self) -> Dict[str, int]:
        """Get statistics about job applications"""
        applications = self.get_job_applications()
        
        stats = {
            'total_applications': len(applications),
            'pending': 0,
            'interview': 0,
            'rejected': 0,
            'offered': 0,
            'accepted': 0
        }
        
        for app in applications:
            # Extra safety check - ensure app is a dictionary
            if isinstance(app, dict):
                status = app.get('status', 'pending').lower()
                if status in stats:
                    stats[status] += 1
            else:
                print(f"Warning: Skipping non-dictionary application: {app}")
        
        return stats
    
    def delete_application(self, app_index: int) -> bool:
        """Delete a specific application"""
        try:
            applications = self.get_job_applications()
            if 0 <= app_index < len(applications):
                applications.pop(app_index)
                
                with open(self.applications_file, 'w') as f:
                    json.dump(applications, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error deleting application: {e}")
            return False
    
    def search_applications(self, search_term: str) -> List[Dict[str, Any]]:
        """Search applications by company name or position"""
        applications = self.get_job_applications()
        search_term = search_term.lower()
        
        results = []
        for app in applications:
            company = app.get('company_name', '').lower()
            position = app.get('position_title', '').lower()
            
            if search_term in company or search_term in position:
                results.append(app)
        
        return results
    
    def get_recent_applications(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent applications"""
        applications = self.get_job_applications()
        
        # Sort by application date (most recent first)
        sorted_apps = sorted(
            applications, 
            key=lambda x: x.get('application_date', ''), 
            reverse=True
        )
        
        return sorted_apps[:limit]


# Test the Data Manager (only runs when file is executed directly)
if __name__ == "__main__":
    print("🧪 Testing Data Manager...")
    
    dm = DataManager()
    
    # Test profile save/load
    print("Testing profile save...")
    test_profile = {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": "Python, JavaScript, SQL",
        "experience": "5 years of software development"
    }
    
    if dm.save_user_profile(test_profile):
        print("✅ Profile saved successfully!")
    else:
        print("❌ Profile save failed!")
    
    print("Testing profile load...")
    loaded_profile = dm.load_user_profile()
    if loaded_profile and loaded_profile.get('name') == 'John Doe':
        print(f"✅ Profile loaded: {loaded_profile['name']}")
    else:
        print("❌ Profile load failed!")
    
    # Test application save
    print("Testing application save...")
    test_app = {
        "company_name": "Tech Corp",
        "position_title": "Python Developer",
        "application_date": datetime.now().isoformat(),
        "status": "pending",
        "job_description": "Looking for a Python developer with 3+ years experience"
    }
    
    if dm.save_job_application(test_app):
        print("✅ Application saved successfully!")
    else:
        print("❌ Application save failed!")
    
    # Test application retrieval
    applications = dm.get_job_applications()
    print(f"✅ Loaded {len(applications)} applications")
    
    # Test stats
    stats = dm.get_application_stats()
    print(f"✅ Stats: {stats}")
    
    print("🎉 Data Manager testing complete!")