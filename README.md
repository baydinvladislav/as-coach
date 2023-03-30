alembic revision --autogenerate -m "nullable fields"
alembic upgrade head

docker-compose build
docker-compose up

The application is a highly specialized CRM for maintaining a client base of fitness trainers.

In a few simple steps, the user can build a training plan and send the file to the client on a mobile device, as well as create new training plans based on the finished one.

No more wasting time manually creating a plan, just a couple of clicks to create a nice-to-read formatted file with a nutrition and training program.

You can see the frontend prototype at the link: https://www.figma.com/proto/l8H9Q4ZCd00mEOV9YPLDlP/Ascoach?page-id=30%3A16481&node-id=418%3A19120&viewport=1023%2C-3966%2C0.51&scaling=scale-down&starting-point-node-id=418%3A19120&show-proto-sidebar=1