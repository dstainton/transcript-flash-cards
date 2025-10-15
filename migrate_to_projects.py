"""
Migration Script: Convert Single-Project to Multi-Project Structure

This script migrates existing flashcard data to the new project-based structure.
It creates a default project and moves all existing data into it.

Safe to run multiple times - checks if migration is needed first.
"""

import os
import shutil
import json
from project_manager import ProjectManager


def migration_needed():
    """Check if migration is needed"""
    # If projects folder exists and has content, migration already done
    if os.path.exists('projects') and os.listdir('projects'):
        return False
    
    # If old files exist, migration is needed
    return (os.path.exists('transcripts') or 
            os.path.exists('flashcards.json') or
            os.path.exists('mastery.json') or
            os.path.exists('history.json'))


def migrate():
    """Perform migration from single-project to multi-project structure"""
    
    print("\n" + "="*60)
    print("MIGRATION: Converting to Multi-Project Structure")
    print("="*60 + "\n")
    
    if not migration_needed():
        print("✓ Migration not needed - projects folder already exists")
        print("  or no existing data found.\n")
        return True
    
    try:
        # Create project manager
        pm = ProjectManager()
        
        # Create default project
        print("1. Creating default project...")
        default_project = pm.create_project("Scrum Certification")
        print(f"   ✓ Created project: {default_project.name}")
        print(f"   ✓ Project folder: {default_project.folder}\n")
        
        # Migrate transcripts folder
        if os.path.exists('transcripts'):
            print("2. Migrating transcripts folder...")
            old_transcripts = 'transcripts'
            new_documents = default_project.documents_folder
            
            # Copy all files from transcripts to documents
            file_count = 0
            for filename in os.listdir(old_transcripts):
                old_path = os.path.join(old_transcripts, filename)
                new_path = os.path.join(new_documents, filename)
                if os.path.isfile(old_path):
                    shutil.copy2(old_path, new_path)
                    file_count += 1
            
            print(f"   ✓ Copied {file_count} files to documents/")
            
            # Rename old folder to keep as backup
            shutil.move(old_transcripts, 'transcripts.backup')
            print(f"   ✓ Original folder backed up as 'transcripts.backup'\n")
        
        # Migrate flashcards.json
        if os.path.exists('flashcards.json'):
            print("3. Migrating flashcards.json...")
            shutil.copy2('flashcards.json', default_project.flashcards_path)
            default_project.load_flashcards()
            print(f"   ✓ Migrated {len(default_project.flashcards)} flashcards")
            
            # Backup original
            shutil.move('flashcards.json', 'flashcards.json.backup')
            print(f"   ✓ Original backed up as 'flashcards.json.backup'\n")
        
        # Migrate mastery.json
        if os.path.exists('mastery.json'):
            print("4. Migrating mastery.json...")
            shutil.copy2('mastery.json', default_project.mastery_path)
            default_project.load_mastery()
            print(f"   ✓ Migrated {len(default_project.mastery)} mastered cards")
            
            # Backup original
            shutil.move('mastery.json', 'mastery.json.backup')
            print(f"   ✓ Original backed up as 'mastery.json.backup'\n")
        
        # Migrate history.json
        if os.path.exists('history.json'):
            print("5. Migrating history.json...")
            shutil.copy2('history.json', default_project.history_path)
            default_project.load_history()
            exam_count = len(default_project.history.get('exam_history', {}))
            study_count = len(default_project.history.get('study_history', {}))
            print(f"   ✓ Migrated {exam_count} exam sessions and {study_count} study sessions")
            
            # Backup original
            shutil.move('history.json', 'history.json.backup')
            print(f"   ✓ Original backed up as 'history.json.backup'\n")
        
        print("="*60)
        print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nYour existing data has been preserved in:")
        print(f"  - {default_project.folder}")
        print("\nOriginal files have been backed up with .backup extension")
        print("You can safely delete the .backup files once you've verified")
        print("everything works correctly.\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR during migration: {e}")
        print("\nMigration failed. Your original files are safe.")
        print("Please report this error.\n")
        return False


if __name__ == '__main__':
    migrate()

