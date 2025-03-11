# customer-chat
Customer Chat Simple App

To run the app simply execute `docker compose up`

Customer UI: http://127.0.0.1/

Support UI: http://127.0.0.1/support

The app is really naive here's the workflow:

* The customer goes to the customer UI and sends some messages
* Support goes then (has to be after customer) and then all pending messages will be seen
* The customer and support can then exchange messages
* If any party leaves the other party will receive a notification
* When a support is connected to a customer, then new customers will have to wait for another support to connect and chat
