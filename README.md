# Help the instructors! (The Ranking Project)

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSKGcxVkIwmU7eOyh27S0Jre8LHj3Morb1hTg&usqp=CAU">
</p>

En este proyecto he utilizado la API de Github (después de autenticarme con el API key) para obtener información acerca de las pull requests realizadas al repositorio de Ironhack "datamad0820".
De esta API he obtenido una lista de pull requests a través de la cual he ido consiguiendo los datos necesarios para obtener de cada lab:
el número de PR abiertas, el número de PR cerradas, el porcentaje de PR completadas (cerradas vs abiertas), el número de PR que faltan por estudiante, la lista de memes únicos usada por cada lab y las horas transcurridas entre el cierre de la PR y el último commit del usuario que la realiza. 

Además, parte de la información obtenida con la API de Github ha sido completada con información extraída mediante web scraping de la propia página del repositorio de Github. Los json formados con dicha información han sido exportados a MongoDB en forma de cuatro colecciones: Labs, Pulls, Users y memes_lst_per_user.
Las colecciones siguen la siguiente estructura (ejemplos):\


**Pulls**:
_id:5f6ce3c414e6dc0539ae6224
users: 
0:"Diegon8"
created_at:"2020-09-21T16:45:52Z"
closed_at:"2020-09-23T23:38:01Z"
last_commit_time:"2020-09-21T16:17:14Z"
instructor_grade_time:55.34638888888889
memes_lst:
0:"https://user-images.githubusercontent.com/68472164/93796393-12fc0e00-f..."
1:"https://user-images.githubusercontent.com/57899051/94084735-8bfb9100-f..."
state:"closed"
pull_id:"490428782"

**Lab**:
_id: ObjectId("5f6ce39514e6dc0539ae61fc")
lab_id:"lab-code-simplicity-efficiency"
pulls_list:
0:"490428782"
1:"488491610"

**Users**:
_id:OBjectId("5f6ce44514e6dc0539ae6445")
name:Diegon8
labs: 
0:"lab-code-simplicity-efficiency"
1:"lab-tableau-data-visualization"

**memes_lst_per_user**:
_id:ObjectId("5f6ce45214e6dc0539ae6460")
name:"Diegon8"
memes_list:
0:"https://user-images.githubusercontent.com/68472164/93796393-12fc0e00-f..."
1:"https://user-images.githubusercontent.com/57899051/94084735-8bfb9100-f..."



Posteriormente, he creado una API usando **Flask**, con una serie de 'endpoints' que vamos a analizar a continuación y que nos permiten llegar al análisis mencionado anteriormente.

## Los 'endpoints' creados han sido los siguientes:

1. **(GET) /student/create/<studentname>** : El propósito es crear un estudiante nuevo y guardarlo en MongoDB. Si intentas meter uno ya existente, no te deja introducirlo.
 Ejemplo: 
  http://localhost:3456/student/create/Marta
  Si no hay ninguna estudiante con ese nombre te añade el nombre de Marta a la lista, pero, en caso de existir saltaría el siguiente error:
  {"Error": "El usuario ya existe"}
 
2. **(GET) /student/all** : El propósito es listar todos los estudiantes existentes en la base de datos. Crea un array con los users de los estudiantes.

Ejemplo: 
  http://localhost:3456/student/all
  
3. **(POST) /lab/create** : El propósito de este endpoint es crear un lab para ser analizado. Los parámetros son el prefijo del lab (entendiendo como prefijo el nombre del mismo). Sigue la misma dinámica que el primer endpoint.

4. **(GET) /lab/<lab_id>/search** : El propósito de este endpoint es buscar la información de un lab concreto como muestro a continuación:
Ejemplo: 
http://localhost:3456/lab/lab-code-simplicity-efficiency/search

  Devuelve: 
  {"lab_id:": "lab-code-simplicity-efficiency", "open_pr_number": 0, "closed_pr_number": 22 "pr_completed_per": 100.0, "unique_memes_list": (la lista de las url de los memes únicos por lab), "user_missing_pr_list": ["FDELTA", "CarlosSanzDGP", "Marta"]}
 
5. **(GET) /lab/memeranking** : El propósito de este endpoint es obtener la lista de los memes más utilizados del repositorio, por cada lab.
Ejemplo: http://localhost:3456/lab/memeranking
Devuelve:el lab id, la lista de las pull requests hechas a ese lab y la lista con los memes.

6. **(GET) /lab/<lab_id>/meme** : El propósito de este endpoint es obtener un meme random extraído de los usados para cada lab.
Ejemplo: 
http://localhost:3456/lab/lab-code-simplicity-efficiency/meme
Devuelve:
"https://user-images.githubusercontent.com/52798316/93581456-7b2fc300-f9a1-11ea-89d2-a953d5c73e88.png"

Este proyecto está diseñado para funcionar desde la terminal.