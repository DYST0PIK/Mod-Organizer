import os
import zipfile
import xml.etree.ElementTree as ET
import config

def mod_organizer():

    # Read the list of installed mods

    for dirpath, dirname, filenames in os.walk(config.mods_directory):

        for a in range(len(filenames)):

            # zipfile_name refers to the .zip file (each mod file) on mods_directory
            # path/FS22_CaseIhPumaT4B.zip

            zipfile_name = str(dirpath+"\\"+filenames[a])

            with zipfile.ZipFile(zipfile_name) as zf:

                content_zip = zf.namelist()

                # Search inside each .zip file for the content that distinguishes each type of mod

                for i in range(len(content_zip)):

                    try:

                        if is_map(content_zip[i]):
                            print("Map: "+zipfile_name)
                            zf.close()
                            os.replace(zipfile_name,("maps"+"\\"+filenames[a]))
                            break

                        elif is_placeable(content_zip[i], zipfile_name):
                            print("Placeable: "+zipfile_name)
                            zf.close()
                            os.replace(zipfile_name,("placeables"+"\\"+filenames[a]))
                            break

                        elif is_vehicle(content_zip[i], zipfile_name):
                            print("Vehicle: "+zipfile_name)
                            zf.close()
                            os.replace(zipfile_name,("vehicles"+"\\"+filenames[a]))
                            break

                    except PermissionError as e:
                        print(f'Permission error: {e}')
                    except FileNotFoundError as e:
                        print(f'File not found: {e}')
                    except Exception as e:
                        print(f'Unexpected error: {e}')

# Functions for mod classification

def is_map(content):

    if content == "maps/":
        return True
    else:
        return False

def is_placeable(content,mod):

    if content == "modDesc.xml":
        with zipfile.ZipFile(mod, 'r') as zip_ref:
            with zip_ref.open(content) as xml_file:

                root = ET.parse(xml_file).getroot()

                for store_item in root.iter('storeItem'):
                    if store_item.get('rootNode') == 'placeable':
                        return True
                    else:
                        return False

def is_vehicle(content,mod):

    if content == "wheels/":
        return True
    elif content == "modDesc.xml":
        with zipfile.ZipFile(mod, 'r') as zip_ref:
            with zip_ref.open(content) as xml_file:

                root = ET.parse(xml_file).getroot()

                for store_item in root.iter('storeItem'):
                    if store_item.get('rootNode') == 'vehicle':
                        return True
                    else:
                        return False

mod_organizer()