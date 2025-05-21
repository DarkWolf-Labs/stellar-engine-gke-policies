#!/usr/bin/env python3

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Create csv file from constraint statuses within the cluster

This tools offers a simple way of gathering the current status of each
constraint on the cluster and outputting it to a csv file for download.

The script is intended to run on the bastion vm with network access to the 
cluster and the output file can then be downloaded.
'''

import subprocess
import csv
import json
import os

def run_kubectl(command):
    """Runs a kubectl command in a Docker container and returns the output."""
    home_dir = os.path.expanduser("~")
    docker_command = [
        "sudo", "docker", "run", "--rm",
        "-v", f"{home_dir}/.kube:/root/.kube",
        "google/cloud-sdk:latest",
        "kubectl"
    ] + command.split()
    try:
        print(f"trying command: {docker_command}")
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
        print("complete")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl command: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def get_constraints_info():
    """Retrieves information about constraints and their status."""
    namespaces_output = run_kubectl("get namespaces -o jsonpath='{.items[*].metadata.name}'")
    if not namespaces_output:
        print("no namespaces")
        return []

    namespaces = namespaces_output.split()
    constraints_info = []


    constraints_output = run_kubectl(f"get constraints -o json")

    try:
        constraints_data = json.loads(constraints_output)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for item in constraints_data.get("items", []):
        constraint_name = item["metadata"]["name"]
        print(item)
        kind = item["kind"]
        constraint_template = item["spec"].get("template", kind)
        status = item.get("status", {})
        violations = status.get("violations", [])
        passing = "PASS" if not violations else "FAIL"
        message = violations[0].get("message", "") if violations else ""

        constraints_info.append({
            "Constraint Name": constraint_name,
            "Constraint Template": constraint_template,
            "Kind": kind,
            "Passing": passing,
            "Message": message.replace(",", ";")  # Replace commas for CSV
        })

    return constraints_info

def write_to_csv(constraints_info, filename="constraints.csv"):
    """Writes constraint information to a CSV file."""
    if not constraints_info:
        print("No constraint data to write.")
        return

    fieldnames = constraints_info[0].keys()

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in constraints_info:
            writer.writerow(row)

    print(f"Data written to {filename}")

if __name__ == "__main__":
    constraints_info = get_constraints_info()
    write_to_csv(constraints_info)