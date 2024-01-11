## The way to create account for coach customers:

**1. Coach Creates Customer Account:**
- The coach initiates the account creation process with a POST request, providing the customer's first name, last name, and Telegram username.

**2. Service Creates Customer Record:**
- The service creates a new customer record in the database, including the provided first name, last name, and Telegram username.
- The service also generates a random, temporary, and not hashed password for the customer.

**3. Delivery of Password for First-Time Login:**
- The application notifies the customer through Telegram about the creation and delivery of a one-time passcode for the initial login.

**4. First Login:**
- When the customer attempts to log in for the first time:
  - The service looks up the customer in the database filter by the temporary password.
  - The system checks if the record is found and matches the customer's first name, last name, Telegram username, and potentially phone number.

**5. Password Change Screen:**
- If the record is found and matches, the system prompts the customer to change their password.
- The service generates a new custom password, hashes it, and stores it securely.

**6. Subsequent Logins:**
- For subsequent logins, the authentication process involves the customer entering their phone number and the newly set password.
- The system authenticates the customer's identity, potentially by checking the hashed password against the stored hash in the database.

**7. Authorization:**
- Upon successful authentication, the system authorizes the customer, allowing them to access to their account.

Simple pseudocode explanation:
```
coach.create_customer(@example_customer_tlg_username, …data)
rep.create(customer with @example_customer_tlg_username)
default_pswd.service.generate_new_pswd(@example_customer_tlg_username)
rep.set(@example_customer_tlg_username, default_pswd)
…
cleint.login(unknown_number, default_pswd)
service.is_default_pswd()
rep.search(default_pswd)
service.match {default_pswd: tlg_username: phone_number}
service.authenticate()
service.hash_password()
service.authorize()
…
```
