from flask import Flask

app = Flask("PullRequest")
@app.route("/")
def html():
    return '''
<!DOCTYPE html>
<html lang="en">
<center>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Help the instructors</title>
</head>
<body style="background-color:#B0C4DE;">
<h1>Introduce cualquiera de los endpoints incluidos en el README</h1>
<a href="https://github.com/AnaMA96/Ranking-Project">Github link</a>
<img src="https://techsalesgroup.files.wordpress.com/2016/10/ironhack-logo-negro1.jpg"/ width="100" height="100">
<form>
    <input type="button" value="Go back" onclick="history.back()">
</form>
</body>
<center>
</html>
'''
