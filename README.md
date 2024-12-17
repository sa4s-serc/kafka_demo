
# Build a simple ML model and set up live data streaming and predictions using Kafka
A demo for implementing and deploying a simple ML model using Kafka and Docker Images
1. Download Docker desktop for your system using the following link
https://www.docker.com/products/docker-desktop/

2. Clone the repository "kafka_demo" to your system using
   ```
   git clone https://github.com/sa4s-serc/kafka_demo/
   ```
3. Open VS code via the terminal (This is purely to see the code)
   

# Choreography style
## Windows 
In the windows command prompt,
### Navigate to the Choreography directory using
```
cd kafka_demo\Choreography
```
###  Create a virtual environment 
```
 python -m venv env
 .\env\Scripts\activate 
```
### Installing Requirements
run the following command :
```
pip install kafka
```
open docker desktop app and sign in and keep it running with this screen as shown below

![image](https://github.com/user-attachments/assets/172fe25b-bee8-4a63-a7f4-5569bf82629e)

Rename the current terminal as "Kafka" by right clicking the title of the terminal
Open two more terminals and rename them as "Producer" and "Consumer" for convenience

### Kafka Terminal
start the Kafka service through docker by running:
```
docker compose up --build
```
### Producer
Navigate to the Choreography directory and activate the same virtual environment using
```
cd kafka_demo\Choreography
.\env\Scripts\activate
cd producer
```
Then install the requirements text using
```
pip install -r requirements.txt
```

### Consumer
Navigate to the Choreography directory and activate the same virtual environment using
```
cd kafka_demo\Choreography
.\env\Scripts\activate
cd consumer
```
Then install the requirements text using
```
pip install -r requirements.txt
```

### Running the simulation

### Producer
```
python producer.py 
```
### Consumer
```
python consumer.py
```


## Linux
### Navigate to the Choreography directory using
```
cd kafka_demo/Choreography
```
###  Create a virtual environment 
```
python3 -m venv env
source ./env/bin/activate
```
### Installing Requirements
run the following command :
```
pip install kafka
```
Start docker on your system by following the instructions from this link:
[https://docs.docker.com/desktop/setup/install/linux/ubuntu/](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)

Open two more terminals- Terminal 2 and Terminal 3

#### First terminal (Current one) - Will be used for Kafka
start Kafka through docker by running:
```
docker compose up --build
```
#### Second terminal  - the Producer terminal 
Activate the same virtual environment created earlier, and then navigate to the producer directory
```
cd kafka_demo/Choreography
source ./env/bin/activate
cd producer
```
Then install the requirements text using
```
pip install -r requirements.txt
```

#### Third terminal - the Consumer terminal
Activate the same virtual environment created earlier, and then navigate to the consumer directory
```
cd kafka_demo/Choreography
source ./env/bin/activate
cd consumer
```
Then install the requirements text using
```
pip install -r requirements.txt
```

### Running the simulation

#### Producer
```
python3 producer.py 
```
#### Consumer
```
python3 consumer.py
```


# Orchestration

## Windows 
In the windows command prompt,
### Navigate to the Orchestration directory using
```
cd kafka_demo\Orchestration
```
###  Create a virtual environment 
```
 python -m venv orc
 .\orc\Scripts\activate 
```
### Installing Requirements
run the following command :
```
pip install -r requirements.txt
```
open docker desktop as an app and sign in and keep it running as shown above.
Rename the current terminal as "Kafka" by right clicking the title of the terminal
Open three more terminals and rename them as "trainer", "orchestrator", and "predictor" for convenience 

### Kafka Terminal
install kafka 
```
pip install kafka-python==2.0.2
```
start Kafka through docker by running:
```
docker compose up --build
```
### Trainer
Activate the same virtual environment using
```
cd kafka_demo\Orchestration
.\orc\Scripts\activate
```

### Orchestrator
Activate the same virtual environment using
```
cd kafka_demo\Orchestration
.\orc\Scripts\activate
```

### Predictor
Activate the same virtual environment using
```
cd kafka_demo\Orchestration
.\orc\Scripts\activate
```

### Running the simulation

### Trainer
```
python trainer.py 
```
### Orchestrator
```
python orchestrator.py
```

### Predictor
```
python predictor.py
```


## Linux
###  Create a virtual environment 
```
cd kafka_demo/Orchestration
python3 -m venv orc
source ./orc/bin/activate
```
### Installing Requirements
run the following command :
```
pip install kafka-python==2.0.2
```
Start docker on your system by following the instructions from this link:
[https://docs.docker.com/desktop/setup/install/linux/ubuntu/](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)

Open three more terminals- Terminal 2, Terminal 3 and terminal 4

#### First terminal (Current one) - Will be used for Kafka
start Kafka through docker by running:
```
docker compose up --build
```
#### Second terminal  - the Trainer terminal 
Activate the same virtual environment created earlier using
```
cd kafka_demo/Orchestrator
source ./orc/bin/activate
```

#### Third terminal - the Consumer terminal
Activate the same virtual environment using
```
cd kafka_demo/Orchestrator
source ./orc/bin/activate
```

#### Fourth terminal - the Consumer terminal
Activate the same virtual environment using
```
cd kafka_demo/Orchestrator
source ./orc/bin/activate
```

### Running the simulation

#### Trainer
```
python3 trainer.py 
```
#### Orchestrator
```
python3 orchestrator.py
```
#### Predictor
```
python3 predictor.py
```



# Other commands for docker



container status check 
```
docker compose ps
```
check logs 
```
docker-compose logs
```
