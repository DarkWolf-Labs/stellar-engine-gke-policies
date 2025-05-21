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
'''Clean exported yaml files of extra elements for application.

This tools offers a simple way of clearing out extra elements like the
'status' block, and timestamps.  The cleaned file can be saved and used 
to be applied as needed.

The script is intended to run on the bastion vm with network access to the 
cluster and the output files can then be downloaded.
'''

import os
import sys

ORIGINAL_YAML_DIRECTORY = "templates"
CLEANED_YAML_DIRECTORY = "cleaned_template_files"

def get_indentation(line_content):
    """Returns the number of leading spaces in a line."""
    return len(line_content) - len(line_content.lstrip(' '))

def remove_status_by_text_filter(input_filepath, output_filepath):
    """
    Reads a YAML file line by line, filters out the blocks that are updated by the system,
    and writes the result to a new file.
    Preserves original formatting.
    Removed blocks: 'status', 'creationTimestamp', 'generation', 'managed-by', 'resourceVersion', 'uid', 'annotations', 'managedFields'

    Returns True if the block was found and lines were skipped, False otherwise.
    """
    print(f"Processing with text filter: {input_filepath}")
    lines_skipped = False
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f_in, \
             open(output_filepath, 'w', encoding='utf-8') as f_out:

            in_status_block = False
            status_block_indentation = -1

            for line in f_in:
                current_indentation = get_indentation(line)
                line_content_stripped = line.lstrip(' ')

                if in_status_block:
                    if current_indentation <= status_block_indentation:
                        in_status_block = False
                        status_block_indentation = -1
                        f_out.write(line)
                    else:
                        lines_skipped = True
                        continue
                elif line_content_stripped.startswith("status:") and current_indentation == 0:
                    in_status_block = True
                    status_block_indentation = current_indentation
                    lines_skipped = True
                    print(f"  Found 'status:' block. Removing...")
                    continue
                elif line_content_stripped.startswith((
                    "creationTimestamp:",
                    "generation",
                    "uid",
                    "resourceVersion",
                )) and current_indentation == 2:
                    in_status_block = False
                    status_block_indentation = current_indentation
                    lines_skipped = True
                    print(f"  Found target line. Removing...")
                    continue
                elif line_content_stripped.startswith("app.kubernetes.io/managed-by:") and current_indentation == 4:
                    in_status_block = True
                    status_block_indentation = current_indentation
                    lines_skipped = True
                    print(f"  Found 'managed-by' line. Removing...")
                    continue
                else:
                    f_out.write(line)

        if lines_skipped:
            print(f"  Successfully processed (lines removed/skipped) and saved to {output_filepath}")
        else:
            print(f"  block not found in {input_filepath}, file copied as is to {output_filepath}")
        return lines_skipped

    except IOError as e:
        print(f"  Error processing file {input_filepath} or {output_filepath}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  An unexpected error occurred processing {input_filepath}: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if not os.path.isdir(ORIGINAL_YAML_DIRECTORY):
        print(f"Error: Input directory '{ORIGINAL_YAML_DIRECTORY}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        os.makedirs(CLEANED_YAML_DIRECTORY, exist_ok=True)
        print(f"Ensured output directory exists: {CLEANED_YAML_DIRECTORY}")
    except OSError as e:
        print(f"Error creating output directory {CLEANED_YAML_DIRECTORY}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nStarting to process YAML files from '{ORIGINAL_YAML_DIRECTORY}' using text filtering...")
    print(f"Cleaned files will be saved in '{CLEANED_YAML_DIRECTORY}'.")
    modified_count = 0
    processed_count = 0

    for filename in os.listdir(ORIGINAL_YAML_DIRECTORY):
        if filename.lower().endswith(('.yaml', '.yml')):
            input_fp = os.path.join(ORIGINAL_YAML_DIRECTORY, filename)
            output_fp = os.path.join(CLEANED_YAML_DIRECTORY, filename)

            if os.path.isfile(input_fp):
                processed_count += 1
                if remove_status_by_text_filter(input_fp, output_fp):
                    modified_count += 1

    print(f"\nFinished processing.")
    print(f"Total YAML files checked: {processed_count}")
    print(f"Files where 'status' block was found and removed: {modified_count}")
    print(f"Check the '{CLEANED_YAML_DIRECTORY}' folder for results.")