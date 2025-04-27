Enable virtual environment: env\Scripts\activate

## Docker

Run docker:
docker run --env-file docker.env -v "C:\University\Honours\Data (temp)\All data with consent\logs from around 2025-03-13 until 2025-04-22:/logs/logs1" -v "C:\University\Honours\Data (temp)\All data with consent\logs from start until 2025-03-09:/logs/logs2" -v "C:\University\Honours\Data (temp)\All data with consent\volumes:/logs/volumes" file-analyser

