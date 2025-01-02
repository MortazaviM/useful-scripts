import requests
import xml.etree.ElementTree as ET
import os

# Fetch and parse XML from a URL
def fetch_and_parse_xml(url):
    current_directory = os.getcwd()
    
    a=[]
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the XML content
        root = ET.fromstring(response.content)
        
        # Iterate through child elements
        for child in root:
            #print(f"Tag: {child.tag}, Attributes: {child.attrib}")
            for subchild in child:
                #print(f"  Subtag: {subchild.tag}, Text: {subchild.text}")
                if len(str(subchild.text)) > 50:
                    a.append(subchild.text)
                    
        for ii in a:
            print(ii)
            new_path = os.path.join(current_directory, "folder", os.path.basename(ii) )
            download_file("https://URL/" + str(ii), new_path)
            
        print(len(a))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching XML: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

def download_file(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Write the content to a file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File downloaded successfully and saved to: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")




# Example usage
url = "https://URL/"  # Replace with your XML URL
fetch_and_parse_xml(url)

