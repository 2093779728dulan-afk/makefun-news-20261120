import os
import shutil
import sys

def main():
    source_path = "assets/entry.png"
    
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.png")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        if not os.path.exists(source_path):
            print(f"Error: Source file '{source_path}' does not exist")
            sys.exit(1)
            
        shutil.copy2(source_path, output_path)
        print(f"Copied {source_path} to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()