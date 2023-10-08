# A Template for Deploying an CI/CD pipeline for a Python web application on the AWS platform
### The appspec.yml, script files, and application files for the deployment
 
This repository contains a template for an CI/CD pipeline for a Python web application on the AWS platform. For the explanation on how to use this template, please refer to the following medium stories.

* [Deploy a Python Application on an AWS CI/CD Pipeline (Part 1): Code Repository](https://medium.com/@andrewlui_60044/deploy-a-python-application-on-a-aws-ci-cd-pipeline-part-1-code-repository-1090ff888eaa)
* [Deploy a Python Application on an AWS CI/CD Pipeline (Part 2): the Application Specification file appspec.yml](https://medium.com/@andrewlui_60044/deploy-a-python-application-on-a-aws-ci-cd-pipeline-part-2-the-application-specification-file-5e3472002be4)
* [Deploy a Python Application on an AWS CI/CD Pipeline (Part 3): the Lot](https://medium.com/@andrewlui_60044/deploy-a-python-application-on-a-aws-ci-cd-pipeline-part-3-the-lot-1849af55db23)

### Requirments
Tested with these versions but older versions may work.
- Python 3.7 or above
- Pandas 1.1.5
- Plotly 5.13.0
- Dash 2.8.1
- Dash Bootstrap Component 1.3.1

### Key Files
- `app.py`: The dashboard web application
- `road_crash.csv`: The trimmed road crash data file extracted from the full set offered at the [Queensland Government Open Data Portal](https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads/resource/e88943c0-5968-4972-a15f-38e120d72ec0)
- `appspec.yml`: The application specification file for the deployment using AWS CodeDeploy
- `scripts/requirements.txt`: The list of Python modules to be installed during the deployment
- `scripts/dash.service': The service specification file to be added as a Linux service.
- 'scripts/install_dependencies.sh`: The script file to execute during the AfterInstall phase of CodeDeploy.
- 'scripts/start_dash.sh': The script file to execute during the ApplicationStart phase of CodeDeploy.
- 'scripts/stop_dash.sh': The script file to execute during the ApplicationStop phase of CodeDeploy.

### The Road Crashes Data File
The application requires the Road Crashes CSV file (`crash_data_queensland_1_crash_locations.csv`), which can be downloaded from the [Open Data Portal](https://www.data.qld.gov.au/dataset/crash-data-from-queensland-roads/resource/e88943c0-5968-4972-a15f-38e120d72ec0) of the Queensland Government, Australia. 

A trimmed version is provided here for testing. Please download the original set if needed.

### Execute the application

Use the `-f` flag to specify the road crash data CSV file.

```
python app.py -f road_crash.csv
```

### Licences

Copyright (C) 2023 - Andrew Kwok-Fai Lui

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see http://www.gnu.org/licenses/.
