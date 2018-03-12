# Log Analysis
Log analysis is a project for the Udacity FullStack Nanodegre. The code execute some queries on a large newspaper company database (> 1000k rows) and extract the following information:
- The three most popular articles of all time
- The most popular article authors of all time
- The days with more than 1% of requests lead to errors


# Pre-requisites
-Python installed (Python 3 recommended)
-Vagrant
-VirtualBox

# Install
## Virtual Machine setup
1. Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
2. To configure the virtual machine, download or clone the repository: git clone https://github.com/udacity/fullstack-nanodegree-vm. Either way, you will end up with a new directory containing the VM files.
3. Change to this directory in your terminal with `cd`. Inside, you will find another directory called vagrant. Change directory to the vagrant directory. Using the command:
  `$ vagrant up`
4. When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `$ vagrant ssh` to log in to your newly installed Linux VM.
5. Inside the VM, change directory to `cd /vagrant`.

## Configure the data
1. Download or clone this repository to the vagrant directory: git clone
2. Download the data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
3. Unzip this file after downloading it. The file inside is called newsdata.sql.
4. Put the newsdata.sql file into the cloned repository (step 1).

## Running the queries:
1. To load the data, use the command `psql -d news -f newsdata.sql`.
1. Run newsdata.py using: `$ python3 newsdata.py`


## License
This project is licensed under the terms of the MIT license.
