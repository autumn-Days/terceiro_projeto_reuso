import os

class FileService:
    """Stateless service to handle File I/O operations"""

    @staticmethod
    def load(filename):
        """Reads a file and returns its content"""
        if not filename:
            raise ValueError("Filename cannot be empty")
        
        try:
            with open(filename, "rt", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to load file: {e}")

    @staticmethod
    def save(filename, content):
        """Writes content to a file. Returns the finalized filename."""
        if not filename:
            raise ValueError("No filename specified")

        # Garante a extensão correta
        final_filename = filename
        if not final_filename.endswith(".writer"):
            final_filename += ".writer"

        try:
            with open(final_filename, "wt", encoding="utf-8") as file:
                file.write(content)
            return final_filename
        except Exception as e:
            raise IOError(f"Failed to save file: {e}")