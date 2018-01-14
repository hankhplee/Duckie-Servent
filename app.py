from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

state = "VELVET"
location = "Leave Home"
environment = {
    "lightness": 0.0,
    "temperature":0.0,
    "humidity":0.0,
    "volume":0.0
}

previousLoc = "Door"
currentLoc = "Room A"
nextLoc = "Room A"
destLoc = "Room A"
action = "STOP"
#currentPath = deque(["A","B","C"])

vetex= ["Room A","Room B","Room C","Door","X","Y","Z"]
parent= [10,10,10,10,10,10,10]
maxint = 10000
distance=[maxint,maxint,maxint,maxint,maxint,maxint,maxint]
boolvertex= [False for i in range(7)]
graph =[[0,0,0,2,0,0,1.5],
        [0,0,0,0,1.5,0,1.5],
        [0,0,0,2,1.5,0,0],
        [2,0,2,0,0,1,0],
        [0,1.5,1.5,0,0,1,0],
        [0,0,0,1,1,0,1],
        [1.5,1.5,0,0,0,1,0],]

def defineshortest(dis, source):
    global boolvertex, distance
    minu = 8
    minint = 10000
    for i in range(7):
        if distance[i] < minint and boolvertex[i]==False :
          minint = distance[i]
          minu   = i
    return minu

def getNextLoc(sol,dis):
    print("Now calculating nextLoc")
    global vetex, parent, distance, boolvertex, graph, maxint
    for i in range(7):
        boolvertex[i] = False
        distance[i] = maxint
    distination = 0
    use = 8
    for i in range(7) :
        if vetex[i] == sol:
            source=i
            break
    for i in range(7) :
        if vetex[i] == dis:
            distination=i
            break
    distance[source]=0
    parent[source]=source
    for i in range(6):
        use = defineshortest(distance,source)
        print("user: ",use)
        boolvertex[use]=True
        for v in range(7):
            if boolvertex[v]==False and graph[use][v]>0 and distance[v]>distance[use]+graph[use][v] :
                 distance[v]= distance[use]+graph[use][v]
                 parent[v]=use
                 #print(distance)
    k = parent[distination]
    if parent[distination] ==source:
        print(vetex[distination])
        return vetex[distination]
    else:
        while 1:
            print("Parent: ",parent[k])
            if parent[k]==source :
                print(vetex[k])
                return vetex[k]
                break
            else :
                k = parent[k]

def update():
    global currentLoc, nextLoc, destLoc, previousLoc
    if(currentLoc != destLoc):
        previousLoc = currentLoc
        currentLoc =  nextLoc

def gardUpdate():
    global currentLoc, nextLoc, destLoc, previousLoc
    previousLoc = currentLoc
    currentLoc =  nextLoc
    if(currentLoc == destLoc):
        if(currentLoc == "Room A"):
            destLoc = "Room B"
        elif(currentLoc == "Room B"):
            destLoc = "Room C"
        elif(currentLoc == "Room C"):
            destLoc = "Door"
        elif(currentLoc == "Door"):
            destLoc = "Room A"
        print("You have arrived ",currentLoc, ". Now go to ",destLoc)

def getNextMove(pre,cur,nxt,dest):
    if(cur == dest):
        return "STOP"
    elif(cur =="Room A"):
        if(pre == "Z" and nxt == "Door"):
            return "STRAIGHT"
        elif(pre == "Door" and nxt == "Z"):
            return "STRAIGHT"
        elif(pre == "Door" and nxt == "Door"):
            return "INVERSE"
        elif(pre == "Z" and nxt == "Z"):
            return "INVERSE"

    elif(cur =="Room B"):
        if(pre == "X" and nxt == "Z"):
            return "STRAIGHT"
        elif(pre == "Z" and nxt == "X"):
            return "STRAIGHT"
        elif(pre == "X" and nxt == "X"):
            return "INVERSE"
        elif(pre == "Z" and nxt == "Z"):
            return "INVERSE"

    elif(cur =="Room C"):
        if(pre == "X" and nxt == "Door"):
            return "STRAIGHT"
        elif(pre == "Door" and nxt == "X"):
            return "STRAIGHT"
        elif(pre == "X" and nxt == "X"):
            return "INVERSE"
        elif(pre == "Door" and nxt == "Door"):
            return "INVERSE"

    elif(cur == "Z"):
        if(pre == "Room A"):
            if(nxt == "Room B"):
                return "RIGHT"
            elif(nxt == "Y"):
                return "STRAIGHT"
            elif(nxt == "Room A"):
                return "INVERSE"
        elif(pre == "Room B"):
            if(nxt == "Room A"):
                return "LEFT"
            elif(nxt == "Room B"):
                return "INVERSE"
            elif(nxt == "Y"):
                return "RIGHT"
        elif(pre == "Y"):
            if(nxt == "Room A"):
                return "STRAIGHT"
            elif(nxt == "Room B"):
                return "LEFT"
            elif(nxt == "Y"):
                return "INVERSE"

    elif(cur == "X"):
        if(pre == "Room B"):
            if(nxt == "Room B"):
                return "INVERSE"
            elif(nxt == "Room C"):
                return "RIGHT"
            elif(nxt == "Y"):
                return "LEFT"
        elif(pre == "Room C"):
            if(nxt == "Room B"):
                return "LEFT"
            elif(nxt == "Room C"):
                return "INVERSE"
            elif(nxt == "Y"):
                return "STRAIGHT"
        elif(pre == "Y"):
            if(nxt == "Room B"):
                return "RIGHT"
            elif(nxt == "Room C"):
                return "STRAIGHT"
            elif(nxt == "Y"):
                return "INVERSE"

    elif(cur == "Y"):
        if(pre == "Door"):
            if(nxt == "Door"):
                return "INVERSE"
            elif(nxt == "X"):
                return "LEFT"
            elif(nxt == "Z"):
                return "STRAIGHT"
        elif(pre == "X"):
            if(nxt == "Door"):
                return "RIGHT"
            elif(nxt == "X"):
                return "INVERSE"
            elif(nxt == "Z"):
                return "STRAIGHT"
        elif(pre == "Z"):
            if(nxt == "Door"):
                return "LEFT"
            elif(nxt == "X"):
                return "STRAIGHT"
            elif(nxt == "Z"):
                return "INVERSE"

    elif(cur == "Door"):
        if(pre == "Room A"):
            if(nxt == "Room A"):
                return "INVERSE"
            elif(nxt == "Room C"):
                return "STRAIGHT"
            elif(nxt == "Y"):
                return "STRAIGHT"
        elif(pre == "Room C"):
            if(nxt == "Room A"):
                return "STRAIGHT"
            elif(nxt == "Room C"):
                return "INVERSE"
            elif(nxt == "Y"):
                return "LEFT"
        elif(pre == "Y"):
            if(nxt == "Room A"):
                return "LEFT"
            elif(nxt == "Room C"):
                return "RIGHT"
            elif(nxt == "Y"):
                return "INVERSE"
    else:
        return "STOP"

@app.route('/')
def dashboard():
    global state, destLoc, currentLoc
    return render_template('dashboard.html', state=state, destination = destLoc,location=currentLoc)

@app.route('/reset', methods=['GET'])
def reset():
    global previousLoc, currentLoc, nextLoc, destLoc, action, state
    previousLoc = "Door"
    currentLoc = "Room A"
    nextLoc = "Room A"
    destLoc = "Room A"
    action = "STOP"
    state = "VELVET"

    return "RESET successful!"

@app.route('/turn', methods=['GET'])
def turn():
    global currentLoc, destLoc, nextLoc, previousLoc, state, action
    #comeFrom = previousLoc
    if(state == "VELVET"):
        if(action != "STOP"):
            update()
        else:
            print("Now Stop")
    else:
        if(action != "STOP"):
            gardUpdate()
        else:
            if currentLoc == "Room A":
                destLoc = "Room B"
            elif currentLoc == "Room B":
                destLoc = "Room C"
            elif currentLoc == "Room C":
                destLoc = "Door"
            elif currentLoc == "Door":
                destLoc = "Room A"
    nextLoc = getNextLoc(currentLoc, destLoc)
    print("NextLoc: ",nextLoc)
    action = getNextMove(previousLoc, currentLoc, nextLoc, destLoc)
    print("From ",previousLoc," Action:",action," Current Location:",currentLoc," Next Location:",nextLoc)
    return action

@app.route('/sendData', methods=['POST'])
def send_data():
    if request.method == 'POST':
        data = request.form['test']
        print(data)
        return data

@app.route('/getCurrentLoc', methods=['GET'])
def getCurrentLoc():
    global currentLoc
    #print(currentLoc)
    return currentLoc

@app.route('/getState', methods=['GET'])
def getState():
    print(state)
    return state

@app.route('/changeState', methods=['POST'])
def changeState():
    global state
    state = request.form['state']
    print(state)
    return render_template('dashboard.html', state=state, destination = destLoc,location=currentLoc)

@app.route('/changeDestination', methods=['POST'])
def changeDestination():
    global destLoc, currentLoc
    destLoc = request.form['location']
    state = "VELVET"
    #updateState()
    print("currentLoc: ",currentLoc, " destLoc: ",destLoc)
    return render_template('dashboard.html', state=state, destination = destLoc,location=currentLoc)

@app.route('/display', methods=['GET'])
def getData():
    global environment
    print(environment)
    return render_template('display.html', environment = environment)
