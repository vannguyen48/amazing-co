Prompt: 

We in Amazing Co need to model how our company is structured so we can do awesome stuff.


We have a root node (only one) and several children nodes,each one with its own children as well. It's a tree-based structure. 


Something like:


         root

        /    \

       a      b

       |

       c


We need two HTTP APIs that will serve the two basic operations:


1) Get all descendant nodes of a given node (the given node can be anyone in the tree structure).

Example request: GET http://127.0.0.1:5000/nodes/a

2) Change the parent node of a given node (the given node can be anyone in the tree structure).

Example request: PUT http://127.0.0.1:5000/nodes/c?new_parent=b

They need to answer quickly, even with tons of nodes. Also,we can't afford to lose this information, so some sort of persistence is required.


Each node should have the following info:


1) node identification

2) who is the parent node

3) who is the root node

4) the height of the node. In the above example,height(root) = 0 and height(a) == 1.

 

We can only have docker and docker-compose on our machines, so your server needs to be run, using them.

Overall Design:

SQL Lite database table `node` for persistence data store. More information are located in app/setup.py

API endpoints are located in app/api.py

Running the app with Docker

Build the docker image: `docker build -t docker-flask:latest . `

Run the app: `docker run --name flaskapp -dt -v$PWD/app:/app -p5000:5000 docker-flask:latest`

Example API calls:

```
vannguyen@MacBook-Pro ~ % curl --location --request GET 'http://0.0.0.0:5000/nodes/b'
{
  "code": 200, 
  "response": "Descendant node(s) of b: c ", 
  "success": "true"
}
vannguyen@MacBook-Pro ~ % curl --location --request GET 'http://0.0.0.0:5000/nodes/a'
{
  "code": 200, 
  "response": "Node a does not have any descendant node.", 
  "success": "true"
}
vannguyen@MacBook-Pro ~ % curl --location --request PUT 'http://127.0.0.1:5000/nodes/c?new_parent=b'
{
  "code": 200, 
  "response": "Updated node c to new parent node b", 
  "success": "true"
}
```