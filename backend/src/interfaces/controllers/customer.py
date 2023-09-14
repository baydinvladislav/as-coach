from fastapi import APIRouter

# TODO: implement separated endpoint to fetch customer plan
# since coach and customer use the same training plan component on the front-end
# we can provide customer access to coach's training plan endpoint
customer_router = APIRouter()
