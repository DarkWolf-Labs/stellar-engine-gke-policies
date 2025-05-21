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
'''Export all current constraint templates on the cluster as yaml.

This tools offers a simple way of gathering the current templates as
a yaml files for download.

The script is intended to run on the bastion vm with network access to the 
cluster and the output files can then be downloaded.
'''

import subprocess
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

templates = [
    'allowedserviceportname',
    'asmauthzpolicydefaultdeny',
    'asmauthzpolicydisallowedprefix',
    'asmauthzpolicyenforcesourceprincipals',
    'asmauthzpolicynormalization',
    'asmauthzpolicysafepattern',
    'asmingressgatewaylabel',
    'asmpeerauthnmeshstrictmtls',
    'asmpeerauthnstrictmtls',
    'asmrequestauthnprohibitedoutputheaders',
    'asmsidecarinjection',
    'destinationruletlsenabled',
    'disallowedauthzprefix',
    'gcpstoragelocationconstraintv1',
    'gkespotvmterminationgrace',
    'k8sallowedrepos',
    'k8savoiduseofsystemmastersgroup',
    'k8sblockallingress',
    'k8sblockcreationwithdefaultserviceaccount',
    'k8sblockendpointeditdefaultrole',
    'k8sblockloadbalancer',
    'k8sblocknodeport',
    'k8sblockobjectsoftype',
    'k8sblockprocessnamespacesharing',
    'k8sblockwildcardingress',
    'k8scontainerephemeralstoragelimit',
    'k8scontainerlimits',
    'k8scontainerratios',
    'k8scontainerrequests',
    'k8scronjoballowedrepos',
    'k8sdisallowanonymous',
    'k8sdisallowedrepos',
    'k8sdisallowedrolebindingsubjects',
    'k8sdisallowedtags',
    'k8sdisallowinteractivetty',
    'k8semptydirhassizelimit',
    'k8senforcecloudarmorbackendconfig',
    'k8senforceconfigmanagement',
    'k8sexternalips',
    'k8shorizontalpodautoscaler',
    'k8shttpsonly',
    'k8simagedigests',
    'k8slocalstoragerequiresafetoevict',
    'k8smemoryrequestequalslimit',
    'k8snoenvvarsecrets',
    'k8snoexternalservices',
    'k8snoownerreference',
    'k8spoddisruptionbudget',
    'k8spodresourcesbestpractices',
    'k8spodsrequiresecuritycontext',
    'k8sprohibitrolewildcardaccess',
    'k8spspallowedusers',
    'k8spspallowprivilegeescalationcontainer',
    'k8spspapparmor',
    'k8spspautomountserviceaccounttokenpod',
    'k8spspcapabilities',
    'k8spspflexvolumes',
    'k8spspforbiddensysctls',
    'k8spspfsgroup',
    'k8spsphostfilesystem',
    'k8spsphostnamespace',
    'k8spsphostnetworkingports',
    'k8spspprivilegedcontainer',
    'k8spspprocmount',
    'k8spspreadonlyrootfilesystem',
    'k8spspseccomp',
    'k8spspselinuxv2',
    'k8spspvolumetypes',
    'k8spspwindowshostprocess',
    'k8spssrunasnonroot',
    'k8sreplicalimits',
    'k8srequireadmissioncontroller',
    'k8srequirebinauthz',
    'k8srequirecosnodeimage',
    'k8srequiredaemonsets',
    'k8srequiredannotations',
    'k8srequiredefaultdenyegresspolicy',
    'k8srequiredlabels',
    'k8srequiredprobes',
    'k8srequiredresources',
    'k8srequirenamespacenetworkpolicies',
    'k8srequirevalidrangesfornetworks',
    'k8srestrictadmissioncontroller',
    'k8srestrictautomountserviceaccounttokens',
    'k8srestrictlabels',
    'k8srestrictnamespaces',
    'k8srestrictnfsurls',
    'k8srestrictrbacsubjects',
    'k8srestrictrolebindings',
    'k8srestrictrolerules',
    'k8sstorageclass',
    'k8suniqueingresshost',
    'k8suniqueserviceselector',
    'noupdateserviceaccount',
    'policystrictonly',
    'restrictnetworkexclusions',
    'sourcenotallauthz',
    'verifydeprecatedapi',
]

for t in templates:
    run_kubectl("get constrainttemplate {t} -n gatekeeper-system -o yaml > constrainttemplates/{t}.yaml")
