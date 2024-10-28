# Reservation Service

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py

docker build -t guest_service .

docker build -t room_inventory_service .

docker build -t reservation_service .


# Run guest_service
docker run -d \
  --name guest_service \
  --network microservice-network \
  -p 5001:5001 \
  guest_service

# Run room_inventory_service
docker run -d \
  -p 5002:5002 \
  --name room_inventory_service \
  --network microservice-network \
  room_inventory_service

# Run reservation_service
docker run -d \
  -p 5003:5003 \
  -e GUEST_SERVICE_URL=http://guest_service:5001 \
  -e ROOM_INVENTORY_SERVICE_URL=http://room_inventory_service:5002 \
  --name reservation_service \
  --network microservice-network \
  reservation_service