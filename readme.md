## 📚 Educados

This project aims to create a very small search engine by indexing IDEB data available at [Resultados Ideb](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados).

The server of the search engine is built using FastAPI and the indexes utilize inverted indexes and TRIEs.
The client is built using Angular.

### ⚙️ Running on development mode

The instructions below assume that you have Node.js and Python, as well as their respective package managers (npm and pip), installed on your computer.

**Client (Angular)**
Navigate to the client folder using your command line.

Run npm install to install the necessary dependencies.

Run npm start to launch the development server.

**Server (Python/FastAPI)**
Navigate to the server folder using your command line.

Run pip install -r requirements.txt to install the required packages.

Execute the main file with Python: python main.py.

**Configuration**
For the application to be fully functional, you must configure the route to the backend in the corresponding files: data-service.ts and dashboard.component.ts.
