# _Site Shepherd_

_Description: Site Shepherd is a Web Site monitoring application that can be run on your local machine to keep tabs on your sites._

## Project Setup

_How do I, as a developer, start working on the project?_ 

1. _Download and run the Selenium Server: http://www.seleniumhq.org/download/._
2. _Update the sites.txt file with a list of sites you wish to monitor._

## Testing

_None yet!_

### Unit Tests

_None yet!_

## Deploying

### _How to deploy_
- _Selenium Server must be running on your machine, download the latest version here: http://www.seleniumhq.org/download/_
- _Execute the jar file like this: `java -jar selenium-server-standalone-2.37.0.jar`_
- _Update the sites.txt file to contain a list of Web Sites that you want to monitor._
- _The following packages are required to run Site Shepherd: requests, selenium, and apscheduler._
- _To install the packages listed above use `sudo easy_install <package>`_
- _Start Site Shepherd by running the shepherd.py file like this: `python shepherd.py`_
- _Logging can be found in the locally created file shepherd.out._

## Troubleshooting & Useful Tools

- _View the log file in the directory you have deployed inside of._

## Contributing changes

- _Please feel free to help contribute to this project through logging issues or submitting pull requests._

## License

- _Site Shepherd uses GPLv2, full license is in the repository._
