# Jira workflow parser
This is a project developed by me, ***Bruno Pereira***, and ***Pietro Lemes*** whose objective is to visualize workflows exported through Jira in the browser, thus eliminating the need to have a Jira instance up and running.

## Getting started
The simplest way to use Jira Workflow Parser is using Docker.
- With [Docker](https://www.docker.com/) installed, download the image with the following command:
- ```docker pull pokkew/jwk:v1```
- Then, you'll need to start a container from that image mapping a port (from the host) to the port 80(of the container) like in the following example (the port 5000 was chosen, however you can any port you want)
- ```docker run -p 5000:80 pokkew/jwk:v1```
- In the browser access the URL http://localhost:5000/ (just replacing 5000 with port number of your choice)

Also, there is a 'lighter' way to run the tool, however it will demand some dependencies:
- Python 3.8
- Graphviz
- Python dependencies:
    - click==8.1.3
    - Flask==2.2.2
    - graphviz==0.20.1
    - itsdangerous==2.1.2
    - Jinja2==3.1.2
    - MarkupSafe==2.1.1
    - pprintpp==0.4.0
    - Werkzeug==2.2.2
    - xmltodict==0.13.0

1. Clone this repository
2. Enter the repository folder
3. Run ``` python app.py ``` 
4. Access the URL http://localhost:80/

## Feedback
looking forward to hear you feedback :blush:
