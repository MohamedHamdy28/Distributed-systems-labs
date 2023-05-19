# Distributed-systems-labs
In this repo, you will find distributed systems projects that I have worked on.

# Lab01, A more reliable file transfer on top of UDP
Lab 1 was about a more reliable file transfer on top of UDP. 
### Client program for sending files
The client program can send two types of messages:

- start message which initiates the file transfer to a given server
- data message which carries part of the file that’s being transferred

The client anticipates an ack message for both of the message types.

1. The client program sends a start message which initiates the file transfer. Its format is as follows:

  s | seqno0 | filename | total_size

  - s indicates that it is start message
  - is a delimiter that divides the neighboring parts in the message
  - seqno0 indicates the start sequence number for messages of this file transfer session; usually, it equals 0
  - filename is the name under which file will be transferred on the server machine, e.g. file1.jpg, resume.txt, etc.
  - total_size is the size of the file being transferred in bytes.

2. If the client receives the ack in response to the start message, it starts transmitting the file by sending data messages one by one. Data message is not longer than the buf_size. Message has the following format:

d | seqno | data_bytes

- d indicates that it is a data message
- seqno is the seqno of this data message; if it’s a first data message, then seqno=seqno0+1; if it’s a second data message then seqno=seqno0+2, etc.
- data_bytes is the part of the file being transmitted. Just raw data

3. When the client receives an ack in response to a data message, it will transmit the next data message if there’s any left.

4. If the client didn't receive ack message for start or data message after 5 retries with 0.5 timeout between them, consider the server to be malfunctioning, terminate the program.

### Server program to receive the files

The server can send only ack messages. The server should have some data structure (e.g., dictionary)
- to hold the file contents it is currently receiving (from different clients) and
- to record the state of the ongoing sessions, e.g: next_seqno, last reception tstamp, expected size, filename, etc.

Other details of the server operation.
1. If the server receives the start message, it replies with an ack message which has the following format:
  a | next_seqno | buf_size
  - a indicates that it is an ack message
  - next_seqno is the sequence number (seqno) of the next message the server is waiting to receive. In this case, next_seqno equals seqno0+1
  - buf_size indicates the maximum size for the data message. Server UDP buffer would be that size.
2. If the server receives the data message, it replies with an ack message which has the following format:
  a | next_seqno
  - a indicates that it is an ack message
  - next_seqno is the sequence number (seqno) of the next message the server is waiting to receive. If it’s waiting for n-th data message, then next_seqno equals     seqno0+n
3. If the server receives duplicate messages from the client, it should respond with an ack message.
4. If the client isn’t active for very long (more than 3s) and the associated file reception session isn’t yet finished, then the server should abandon this session and remove everything related to it.
5. The server should hold the information related to the successfully finished file reception for some time (1.0s) before finally removing it.

# Lab02, Multithreaded client-server socket programming

Create a server and client application using TCP sockets and multithreading
1. The client sends the numbers to the server one by one.
2. The server checks if the number is prime or not and sends the result to the client.
3. The client prints the result.

### Client
1. Client has a list of numbers to process.
2. Client takes a number, sends it to the server and prints the result.
3. Has a command line argument:
- ip-addr:port-number of the server Example: python3 client.py 127.0.0.1:5555

If the server is not available at the start of the client, or at any time during data transmission, terminate
the client.

Connection must be implemented via TCP sockets.

Numbers to process:
numbers = [15492781, 15492787, 15492803,
15492811, 15492810, 15492833,
15492859, 15502547, 15520301,
15527509, 15522343, 1550784]

### Server

1. Main thread creates several worker threads.
2. After that, the main thread continuously listens for connections from clients. The server must be able to stop, when the KeyboardInterrupt (Ctrl+C in console) is raised.
3. When a new connection is accepted, main thread passes it to one of worker thread.
4. Worker thread continues the work with the client.
5. When the server stops, all worker threads must be stopped.
6. The server must be able to process several client connections at the same time (at least 2).
7. Has a command line argument:
- port-number to listen on. Example: python3 server.py 5555

You should use Thread from the threading module and Queue from the multiprocessing module.
- When the main thread accepts a connection, it puts a connection socket and an address in the queue.
- Worker thread continuously checks the queue. If it's not empty, it takes an element (connection information) and processes this connection.

# Lab03, using ZeroMQ to organize a distributed system

### Client:
1) Connect to server ZeroMQ sockets: client_inputs, client_outputs
2) Read a line from the terminal
3) Send line to ZeroMQ
4) Receive a message from client_outputs and print it

### Server:
1) Binds ZeroMQ sockets: client_inputs, client_outputs, worker_inputs, worker_outputs
2) Receive message from the client_inputs, send the message to worker_inputs
3) Receive message from worker_outputs, send message to client_outputs

### Prime:
1) connects to ZeroMQ sockets: worker_inputs, worker_outputs
2) Receive message from the worker_inputs
3) If message has following format “isprime N” then test number N for primeness
4) Send result to worker_outputs: “N is prime” or “N is not prime”

### GCD
1) connects to ZeroMQ sockets: worker_inputs, worker_outputs
2) Receive message from the worker_inputs
3) If message has following format “gcd A B” then computes Greatest Common
Divisor for given two integers
4) Send result to worker_outputs: “gcd for A B is C”

![image](https://github.com/MohamedHamdy28/Distributed-systems-labs/assets/71794972/b6d186f5-ca3a-4240-9ebc-40ea6c366179)

# Lab04, develop a server and a client using gRPC

### Server
python3 server.py 5555

Has following functions:

- reverse(text: str) -> str – returns reversed string
- split(text: str, delim:str) -> (int, [str]) – splits the text by delimiter. Returns number of parts and parts themself
- isprime(num: int) -> str – checks if number is prime or not. This is a stream function, which means it accepts a stream of numbers and returns a stream of answers

Server must support multiple clients

### Client

python3 client.py 127.0.0.1:5555

Continuously listens to client input and executes commands:
- reverse <some text> – rpc call
- split <some text> – rpc call – split text by whitespaces
- isprime <list of numbers> – rpc call 
  Example: isprime 2 10 5555 14567
- exit – stops loop and exits program
  
# Lab05, implement chord distributed hash table
You have to implement a simplified version of the chord distributed hash table using grpc
and protobuf.  

### Example:

``` 
python Registry.py 127.0.0.1:5000 5
python3 Node.py 127.0.0.1:5000 127.0.0.1:5001
python3 Node.py 127.0.0.1:5000 127.0.0.1:5002
python3 Node.py 127.0.0.1:5000 127.0.0.1:5003
python3 Node.py 127.0.0.1:5000 127.0.0.1:5004
python3 Node.py 127.0.0.1:5000 127.0.0.1:5005
python3 Node.py 127.0.0.1:5000 127.0.0.1:5006
```

Nodes are going to request the registry to give them an id. As they spawn one after another
they connect to their neighbors as successors and predecessors:

```
assigned node_id=24, successor_id=24, predecessor_id=24
assigned node_id=26, successor_id=24, predecessor_id=24
assigned node_id=2, successor_id=24, predecessor_id=26
assigned node_id=16, successor_id=24, predecessor_id=2
assigned node_id=31, successor_id=2, predecessor_id=26
assigned node_id=25, successor_id=26, predecessor_id=24
```
![image](https://github.com/MohamedHamdy28/Distributed-systems-labs/assets/71794972/b5511385-10a0-43e1-84d8-56d1d8ee1774)

Okay, now the network is up, we can try to store key-value data.

``` 
  connect 127.0.0.1:5000 
  get_info
  24: 127.0.0.1:5001
  26: 127.0.0.1:5002
  2: 127.0.0.1:5003
  16: 127.0.0.1:5004
  31: 127.0.0.1:5005
  25: 127.0.0.1:5006  
```
![image](https://github.com/MohamedHamdy28/Distributed-systems-labs/assets/71794972/1cbf4f7c-a214-4f5f-ac84-bc82f5c24471)

# Lab 6, implement RAFT (Leader election)

In this assignment you have to implement a part of RAFT protocol.
This part is a leader election.
To do so, you must use gRPC.

### Term

- The life cycle of the system is divided into terms.
- Each term starts with the election.
- Term number is starting at 0 and increases by 1 each term (in election round).

### Configuration file

- Contains information about the system in the format: id address port.
- The number of lines means the number of servers (nodes) in the system.
- Has the name config.conf.

## Server

Server has its own:
1. term number - 0 at the startup. Increases by 1 in each election round.
2. timer - initialized at the startup with a random value in the range [150, 300] ms.
3. Information about other servers: their total number, and their addresses (from config file).

### Startup

Has one command line argument: id.

At the start, server reads the config file, finds the corresponding address and the port number, and binds to it. Also, it prints the address and port to which it is bound.

### States
Three possible states: Follower, Candidate or Leader

**Note:** reset timer means it start counting from the beginning. It does not re-initilize timer with a new random timeout.

**Important:** If server receives a term number greater than its own (in any message), it should update its term
number.

Follower - the initial state of the server.

- Every time Follower receives any message from the Leader, it resets the timer.
- If the timer is expired, Follower becomes a Candidate.
- If it receives a RequestVote message, it must vote for a given Candidate, if it has not already voted in that term. I.e. it can vote only once in a single term.

  
Candidate - trying to become a leader.

- First, it increments its term number and resets its timer.
- Then, it requests votes from all other nodes. Also, this Candidate votes for itself.

Possible outcomes:

1. If it has the majority of votes before its timer is up, the Candidate becomes a Leader.
2. If the timer is up, and the Candidate does not have the majority of votes, it generates a new timer (with the new random time) and becomes a Follower.
3. If the Candidate receives the message (any message) with the term number greater than its own, it stops the election and becomes a Follower. Also, it should update its term number with received term in this case.
  
Leader - runs the system.

- Every 50 milliseconds sends an AppendEntries request to all other servers. This is the heartbeat message.

- If the Leader receives a heartbeat message from another Leader with the term number greater than its own, it becomes a Follower (and also sets its term number to the new leader's one).

### Functions
The server has the following RPC functions:
1. RequestVote
2. AppendEntries
3. GetLeader
4. Suspend

the rest can be found here: https://drive.google.com/file/d/1YgoiEwFIrmI5VEI0RPpgE5VJE0bkZY1p/view?usp=sharing
  




















