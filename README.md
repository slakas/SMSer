# SMSer
> Simple script for receiving an alert from Grafana and send them into SMS gateway
<hr>

## Description

The program is listening on 'POST' call, checking authentication, parsing JSON, and sent it into SMS gateway using SOAP call. <br />
It is useful for Grafana alerting.

## Installation
Just clone the git and install all requirements if needed

## How to use
Edit config file (`conf.cnf`) for your environment 
 > ` python3 listener.py `


