from RedeemPoint import RedeemPoint
import json
from flask import Flask, request, jsonify
app = Flask(__name__)
dataList=[]

# Helper function
def mapResult(x):
    keys = [key for key in x.keys()]
    values=[value for value in x.values()]
    return {'payer': keys[0], 'points':values[0]}

# Add balance
# use: http://localhost:8000/add
@app.route("/add",methods=['POST'])
def addPoints():
    data = request.get_json()
    rp = RedeemPoint(data["payer"],data["points"],data["timestamp"]);
    dataList.append(rp);
    return "Ok",200

# Spend points
# use: http://localhost:8000/spend
@app.route("/spend",methods=['POST'])
def spendPoints():
    redeemPoint = request.get_json()
    sortedData = sorted(dataList, key=lambda x: x.timestamp)
    # check if possible to redeem
    totalRedeemPoint = redeemPoint["points"];
    deductionPoints = {}    
    availblePoints=0;

    for item in sortedData:
        availblePoints = availblePoints +  item.point
        
    if availblePoints<totalRedeemPoint:
        return "Exceed the available balance!",404

    i = 0
    len_list = len(sortedData)
    while i < len(sortedData):
        currentPoint = sortedData[i].point;
        nextPoint = 0
        if (i+1) < len_list:
            nextPoint = sortedData[i+1].point;
        
        if nextPoint<0:
            totalRedeemPoint = totalRedeemPoint + abs(nextPoint);

        if totalRedeemPoint <= currentPoint:
            remainPoint = abs(currentPoint - totalRedeemPoint)
            deductionPoints[sortedData[i].payer]= - totalRedeemPoint;
            totalRedeemPoint = 0
            sortedData[i].point= remainPoint;
        
        if totalRedeemPoint > currentPoint:
            sortedData[i].point=0;
            deductionPoints[sortedData[i].payer] = -currentPoint;
            totalRedeemPoint = totalRedeemPoint - currentPoint    

        if currentPoint <= 0:
            totalRedeemPoint = totalRedeemPoint + abs(currentPoint);
            sortedData[i].point=0;
            i = i + 1
            continue;

        if totalRedeemPoint <= currentPoint:
            remainPoint = abs(currentPoint - totalRedeemPoint)
            deductionPoints[sortedData[i].payer]= - totalRedeemPoint;
            totalRedeemPoint = 0
            sortedData[i].point= remainPoint;
        
        if totalRedeemPoint > currentPoint:
            sortedData[i].point=0;
            deductionPoints[sortedData[i].payer] = -currentPoint;
            totalRedeemPoint = totalRedeemPoint - currentPoint  

        if totalRedeemPoint==0:
            break
        i = i + 1
    # The only thing is map isn't working
    #listPoints = list(map(mapResult, deductionPoints));

    return jsonify(deductionPoints),200

# get balance
# use: http://localhost:8000/balance
@app.route("/balance",methods=['GET'])
def displayPoints():

    sortedData = sorted(dataList, key=lambda x: x.timestamp)
    grouped_items = {}
    for item in sortedData:
        category = item.payer
        value = item.point
        grouped_items[category] = grouped_items.get(category, 0) + value

    # Return a JSON response
    return jsonify(grouped_items)

# Get the added point list
# use: http://localhost:8000/pointlist
@app.route("/pointlist",methods=['GET'])
def displayPointList():
    sortedData = sorted(dataList, key=lambda x: x.timestamp)
    # Return a JSON response
    return jsonify([ob.to_json() for ob in sortedData])


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8000)

