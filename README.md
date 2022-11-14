## Setup

### Front end
Front end uses `Vue` + `vite`.
Navigate to project directory and run:
```shell
npm i 
npm run dev
```
This should launch the application at `localhost:5173` (port number may vary). 

### Back end
Back end uses `flask` in python. 
First setup the environment by running:
```shell
# env.yml is under src/server/
conda env create -f env.yml
```
To launch the server, navigate to src/server/ and run:
```
flask --app server run
```
The default server address is `localhost:5000`. 





