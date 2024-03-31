import os
import shutil
import atexit

def clean_pycache():
    for root, dirs, files in os.walk(".", topdown=True):
        for dir in dirs:
            if dir == "__pycache__":
                pycache_path = os.path.join(root, dir)
                try:
                    for item in os.listdir(pycache_path):
                        item_path = os.path.join(pycache_path, item)
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        else:
                            shutil.rmtree(item_path)
                    os.rmdir(pycache_path)
                    print(f"Deleted {pycache_path}")
                except OSError as e:
                    print(f"Failed to delete {pycache_path}: {e}")

atexit.register(clean_pycache)
