import uuid
class RedeemPoint:
    def __init__(self, payer, point,timestamp):
        self.payer = payer
        self.point = point
        self.timestamp = timestamp
        self.id = uuid.uuid4()
  
    # explicit function      
    def to_json(self):
        return {
                'payer': self.payer,
                'point': self.point,
                'timestamp':self.timestamp
            }