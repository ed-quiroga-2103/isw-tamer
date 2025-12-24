

DEFAULT_CONFIG = "./assets/default-config.conf"
IGNORE_LINE_CHAR = "#"

KEY_EXCLUSIONS = ["[MSI_ADDRESS_DEFAULT]", "[USB_BACKLIGHT]", "[COOLER_BOOST]"]

import re

header_regex = re.compile(r"^\[(.+)\]$")

def parse_config():
    sections = {}
    current_key = None
    with open(DEFAULT_CONFIG) as f:
        lines = [
                line.strip()
                for line in f
                # if not line.startswith(IGNORE_LINE_CHAR) and line.strip()
            ]

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line in KEY_EXCLUSIONS:
                continue

            match = header_regex.match(line)

            

            if match:
                current_key = f"[{match.group(1)}]"
                sections[current_key] = []
                continue

            if current_key:
                sections[current_key].append(line)
        return sections
    


def get_models(values, clean_key):

    models = []

    for line in values:

        line = re.sub(r'\([^)]*\)', '', line) # Removes content between parenthesis

        if "#" in line and clean_key not in line and line not in ["# GPU", "# CPU"]: # Skips invalid lines
            clean_line = line.replace("# ","").strip()
            line_models = clean_line.split(" ")
            models += line_models

    return models


def get_value_lines(values, hardware, type):

    lines = []
    for line in values:


        my_regex = re.escape(f"{hardware}_{type}_") + r"[0-9]{1}"

        

        if re.search(my_regex, line):            
            lines.append(line)

    return lines




def edit_line(line, new_value):
    new_line = re.sub(r"(\d+)$", new_value, line)
    return new_line




def main():

    data = parse_config()

    for key, values in data.items():
        
        clean_key = key.replace("[","").replace("]","")
        models = get_models(values, clean_key)
        
        cpu_temps = get_value_lines(values, 'cpu', 'temp')
        cpu_speeds = get_value_lines(values, 'cpu', 'speed')

        gpu_temps = get_value_lines(values, 'gpu', 'temp')
        gpu_speeds = get_value_lines(values, 'gpu', 'fan_speed')


        gpu_speeds[6] = edit_line(gpu_speeds[6], "100")

        print("\nSECTION: ", key)
        
        print("\nModels:\n")
        print(" - ".join(models))

        print("\nCPU Temps:\n") 
        print("\n".join(cpu_temps))
        print("\nCPU Speeds:\n")
        print("\n".join(cpu_speeds))
        print("\nGPU Temps:\n") 
        print("\n".join(gpu_temps))
        print("\nGPU Speeds:\n") 
        print("\n".join(gpu_speeds))
        




main()

