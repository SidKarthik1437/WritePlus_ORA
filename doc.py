import os
from docx import Document

# Folder path containing the DOCX files
folder_path = './reports/'

# Create a new document
combined_doc = Document()

# Iterate through the files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.docx'):
        file_path = os.path.join(folder_path, file_name)
        
        # Open each file and copy its content to the combined document
        doc = Document(file_path)
        for element in doc.element.body:
            combined_doc.element.body.append(element)

# Save the combined document
combined_doc.save('./combined.docx')
