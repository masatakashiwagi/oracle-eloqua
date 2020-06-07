# Eloqua Python-Wrapper
Version: Python 2.7.13<br>

Oracle Eloqua is one of the marketing automation tools.<br>
I implemented API programs which you can export some data.<br>
There is no import function so far.<br>

you need to set some info for your Eloqua instance.
```python
sitename = 'your sitename'
username = 'your username'
password = 'your password'
client = Eloqua_Request(sitename, username, password, mode="REST")
```
