"""
Project Management System for Flash Cards Application

Handles multiple projects, each with their own documents, flashcards,
mastery tracking, and statistics.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional


class Project:
    """Represents a single flashcard project"""
    
    def __init__(self, project_id: str, name: str, folder_path: str):
        self.id = project_id
        self.name = name
        self.folder = folder_path
        self.flashcards = []
        self.mastery = {}
        self.excluded = {}
        self.history = {'exam_history': {}, 'study_history': {}, 'all_time_scores': {}}
        
        # Ensure project folder structure exists
        self._ensure_folder_structure()
    
    def _ensure_folder_structure(self):
        """Create project folder structure if it doesn't exist"""
        os.makedirs(self.folder, exist_ok=True)
        os.makedirs(os.path.join(self.folder, 'documents'), exist_ok=True)
    
    @property
    def flashcards_path(self) -> str:
        return os.path.join(self.folder, 'flashcards.json')
    
    @property
    def mastery_path(self) -> str:
        return os.path.join(self.folder, 'mastery.json')
    
    @property
    def excluded_path(self) -> str:
        return os.path.join(self.folder, 'excluded.json')
    
    @property
    def history_path(self) -> str:
        return os.path.join(self.folder, 'history.json')
    
    @property
    def project_meta_path(self) -> str:
        return os.path.join(self.folder, 'project.json')
    
    @property
    def documents_folder(self) -> str:
        return os.path.join(self.folder, 'documents')
    
    def load_flashcards(self) -> List[Dict]:
        """Load flashcards from project folder"""
        try:
            if os.path.exists(self.flashcards_path):
                with open(self.flashcards_path, 'r', encoding='utf-8') as f:
                    self.flashcards = json.load(f)
                    # Add answer_type to existing flashcards if missing
                    for card in self.flashcards:
                        if 'answer_type' not in card:
                            card['answer_type'] = self._get_answer_type(card.get('answer', ''))
                return self.flashcards
        except Exception as e:
            print(f"Error loading flashcards for project {self.name}: {e}")
        return []
    
    def save_flashcards(self):
        """Save flashcards to project folder"""
        try:
            with open(self.flashcards_path, 'w', encoding='utf-8') as f:
                json.dump(self.flashcards, f, indent=2)
        except Exception as e:
            print(f"Error saving flashcards for project {self.name}: {e}")
    
    def load_mastery(self) -> Dict:
        """Load mastery data from project folder"""
        try:
            if os.path.exists(self.mastery_path):
                with open(self.mastery_path, 'r', encoding='utf-8') as f:
                    self.mastery = json.load(f)
                return self.mastery
        except Exception as e:
            print(f"Error loading mastery for project {self.name}: {e}")
        return {}
    
    def save_mastery(self):
        """Save mastery data to project folder"""
        try:
            with open(self.mastery_path, 'w', encoding='utf-8') as f:
                json.dump(self.mastery, f, indent=2)
        except Exception as e:
            print(f"Error saving mastery for project {self.name}: {e}")
    
    def load_excluded(self) -> Dict:
        """Load excluded cards data from project folder"""
        try:
            if os.path.exists(self.excluded_path):
                with open(self.excluded_path, 'r', encoding='utf-8') as f:
                    self.excluded = json.load(f)
                return self.excluded
        except Exception as e:
            print(f"Error loading excluded cards for project {self.name}: {e}")
        return {}
    
    def save_excluded(self):
        """Save excluded cards data to project folder"""
        try:
            with open(self.excluded_path, 'w', encoding='utf-8') as f:
                json.dump(self.excluded, f, indent=2)
        except Exception as e:
            print(f"Error saving excluded cards for project {self.name}: {e}")
    
    def load_history(self) -> Dict:
        """Load history from project folder"""
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # Convert string dates back to datetime objects
                    from datetime import datetime
                    self.history = {
                        'exam_history': {
                            datetime.fromisoformat(k): v 
                            for k, v in history.get('exam_history', {}).items()
                        },
                        'study_history': {
                            datetime.fromisoformat(k): v 
                            for k, v in history.get('study_history', {}).items()
                        },
                        'all_time_scores': history.get('all_time_scores', {})
                    }
                return self.history
        except Exception as e:
            print(f"Error loading history for project {self.name}: {e}")
        return {'exam_history': {}, 'study_history': {}, 'all_time_scores': {}}
    
    def save_history(self):
        """Save history to project folder"""
        try:
            # Convert datetime objects to ISO format strings
            history_to_save = {
                'exam_history': {
                    k.isoformat() if isinstance(k, datetime) else k: v 
                    for k, v in self.history.get('exam_history', {}).items()
                },
                'study_history': {
                    k.isoformat() if isinstance(k, datetime) else k: v 
                    for k, v in self.history.get('study_history', {}).items()
                },
                'all_time_scores': self.history.get('all_time_scores', {})
            }
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(history_to_save, f, indent=2)
        except Exception as e:
            print(f"Error saving history for project {self.name}: {e}")
    
    def save_metadata(self):
        """Save project metadata"""
        metadata = {
            'id': self.id,
            'name': self.name,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat()
        }
        try:
            with open(self.project_meta_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"Error saving metadata for project {self.name}: {e}")
    
    def get_stats(self) -> Dict:
        """Get project statistics"""
        topics = sorted(set(card['topic'] for card in self.flashcards)) if self.flashcards else []
        stats = {
            'total_flashcards': len(self.flashcards),
            'mastered_count': len(self.mastery),
            'excluded_count': len(self.excluded),
            'mastery_percentage': (len(self.mastery) / len(self.flashcards) * 100) if self.flashcards else 0,
            'total_topics': len(topics),
            'total_sessions': len(self.history.get('study_history', {})) + len(self.history.get('exam_history', {})),
            'topics': topics
        }
        return stats
    
    def _get_answer_type(self, correct_answer: str) -> str:
        """Determine the type of answer expected"""
        answer_lower = correct_answer.strip().lower()
        if answer_lower in ['true', 'false']:
            return 'true_false'
        elif answer_lower in ['yes', 'no']:
            return 'yes_no'
        elif len(correct_answer.split()) == 1 and correct_answer.isalpha() and len(correct_answer) == 1:
            return 'multiple_choice'
        elif ',' in correct_answer and all(len(part.strip()) == 1 and part.strip().isalpha() for part in correct_answer.split(',')):
            return 'multiple_answer'
        else:
            return 'multiple_choice'


class ProjectManager:
    """Manages all flashcard projects"""
    
    def __init__(self, projects_root: str = 'projects'):
        self.projects_root = projects_root
        self.projects: Dict[str, Project] = {}
        self._ensure_projects_folder()
        self._load_all_projects()
    
    def _ensure_projects_folder(self):
        """Create projects root folder if it doesn't exist"""
        os.makedirs(self.projects_root, exist_ok=True)
    
    def _load_all_projects(self):
        """Load all existing projects from the projects folder"""
        try:
            if not os.path.exists(self.projects_root):
                return
            
            for folder_name in os.listdir(self.projects_root):
                folder_path = os.path.join(self.projects_root, folder_name)
                if os.path.isdir(folder_path):
                    meta_path = os.path.join(folder_path, 'project.json')
                    if os.path.exists(meta_path):
                        try:
                            with open(meta_path, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                                project = Project(
                                    metadata['id'],
                                    metadata['name'],
                                    folder_path
                                )
                                self.projects[project.id] = project
                        except Exception as e:
                            print(f"Error loading project from {folder_path}: {e}")
        except Exception as e:
            print(f"Error loading projects: {e}")
    
    def create_project(self, name: str) -> Project:
        """Create a new project"""
        # Generate unique project ID
        project_id = self._generate_project_id(name)
        
        # Create project folder
        folder_path = os.path.join(self.projects_root, project_id)
        
        # Create project
        project = Project(project_id, name, folder_path)
        project.save_metadata()
        
        # Add to projects dict
        self.projects[project_id] = project
        
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID"""
        return self.projects.get(project_id)
    
    def list_projects(self) -> List[Dict]:
        """List all projects with their metadata"""
        project_list = []
        for project in self.projects.values():
            stats = project.get_stats()
            project_list.append({
                'id': project.id,
                'name': project.name,
                'total_flashcards': stats['total_flashcards'],
                'mastery_percentage': stats['mastery_percentage'],
                'total_sessions': stats['total_study_sessions'] + stats['total_exam_sessions']
            })
        return sorted(project_list, key=lambda x: x['name'])
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        import shutil
        
        if project_id not in self.projects:
            return False
        
        try:
            project = self.projects[project_id]
            # Remove project folder
            if os.path.exists(project.folder):
                shutil.rmtree(project.folder)
            # Remove from projects dict
            del self.projects[project_id]
            return True
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False
    
    def _generate_project_id(self, name: str) -> str:
        """Generate a unique project ID from name"""
        # Create URL-friendly ID
        base_id = name.lower().replace(' ', '-')
        base_id = ''.join(c for c in base_id if c.isalnum() or c == '-')
        
        # Ensure uniqueness
        project_id = base_id
        counter = 1
        while project_id in self.projects:
            project_id = f"{base_id}-{counter}"
            counter += 1
        
        return project_id

