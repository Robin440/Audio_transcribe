import os

def delete_file(file_path):
    try:
        # Check if file exists
        if os.path.exists(file_path):
            os.remove(file_path)
            return  True
        else:
            return False
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
