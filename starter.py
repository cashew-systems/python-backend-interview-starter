import sqlalchemy

# TODO: Write the tests case, make sure I can get the first two test cases to pass

# Util function
def executeQuery(query):
  if "insert" in query.lower():
    if query[-1] == ";":
      query = query[:-1]
    query = query + " returning id"
  engine = sqlalchemy.create_engine("postgresql://coderpad:@/coderpad?host=/tmp/postgresql/socket")
  connection = engine.connect()
  result = connection.execute(query)
  return result.fetchall()

# Implementation

#  Challenge one: Implement cursor based pagination
#
#  Path: GET /employees
#
#  Parameters:
#    page_before
#    page_after
#    page_size
#
#  returns:
#    employee[] employees
#    next_cursor = foobar
#
#
#   Tasks to implement endpoint:
#       1. Implement returning pageSize results with pageAfter specified
#       2. Implement returning pageSize results with pageBefore specified
#       3. Add better error handling for both SQL errors and parameters
#

def getEmployees(path, queryString, headers, body):
  response = {}
  response["employees"] = executeQuery("select * from employees")
  return response
  # Read employees from the database and return them all

#
#  Challenge two: Implement payroll-run endpoint
#
#  Path: /payroll-run
#
#  Body:
#    hours_worked
#
#  returns:
#    none
#
# Tasks to implement endpoint:
#  1. Create payroll_run object in PENDING state
#  2. Calcualte rate for all employees with hourly pay records
#  3. Save the payment contributing in this table
#  4. Return 200 to client
#  5. Basic error cases and error handling
#

def postPayrollRun(path, queryString, headers, body):
  pass
#
#   Challenge three:  Add employee payment to existing payroll run
#
#   Tasks to implement:
#
#      1. Add the new payment to the payments for the run
#      2. Implement API level idempotency (hint: you can modify request parameters)
#
#   Error cases:
#
#      1. Employee ID is not valid
#      2. Payroll run ID is not valid
#      3. One of the database requests fails, what happens if we're in a partial failure state?
#
#
#
#  Path:
#     /payroll-run/{id}/employee-payment/{employee_id}
#
#   Body:
#      amount: number
#      paymentMemo: text
#
#   Return:
#      none
#

def postPayrollRunEmployeePayment(path, queryString, headers, body):
  pass

#
#
#  Challenge four:  Add employee payment to existing payroll run
#  Path:
#   /payroll-run/{id}/finalize-run
#
#  Body:
#      None
#
#  Returns:
#      //TODO: Challenge what should this return?
#
#  Tasks to implement endpoint
#
#  1.  Change status of payroll run from PENDING to COMPLETE
#  2.  Implement immediate response to client
#  3.  Implement (or discuss if not time) ability for client to find out result of endpoint after immediate response
#  4.  Discuss solutions to error cases
#
#
#  Error cases
#
#  1. Payroll run id is not a PENDING payroll run
#  2. After immediate response is given, the processing of payroll fails and must be resubmitted.
#

def postPayrollRunFinalizeRun(path, queryString, headers, body):
  pass

def getEmployeesTestOne():
  requestPath = "/employees"
  requestQueryString = {}
  requestHeaders = {}
  requestBody = {}
  result = getEmployees(requestPath, requestQueryString, requestHeaders, requestBody)     
  employees = result["employees"]
  assert len(employees) == 4, "There were not four employees returned"
  assert employees[0].name == "David", "David was not the first employee"

def getEmployeesTestTwo():
  requestPath = "/employees"
  requestQueryString = {}
  requestHeaders = {}
  requestBody = {}

  requestBody["page_size"] = 2
  requestBody["page_before"] = 1

  result = getEmployees(requestPath, requestQueryString, requestHeaders, requestBody)     
  employees = result["employees"]
  assert len(employees) == 2 , "Cursor test two: The wrong number of employees was returned"
  assert employees[0]["name"] == "Anthony" , "Cursor test two: The wrong first employee was returned"
  assert employees[1]["name"] == "Aman" , "Cursor test two: The wrong second employee was returned"

def getEmployeesTestThree():
  requestPath = "/employees"
  requestQueryString = {}
  requestHeaders = {}
  requestBody = {}

  requestBody["page_size"] = 2
  requestBody["page_after"] = 4

  result = getEmployees(requestPath, requestQueryString, requestHeaders, requestBody)     
  employees = result["employees"]
  assert len(employees) == 2 , "Cursor test three: The wrong number of employees was returned"
  assert employees[0]["name"] == "Aman" , "Cursor test three: The wrong first employee was returned"
  assert employees[1]["name"] == "Anthony" , "Cursor test three: The wrong second employee was returned"

def getEmployeesTestFour():
  requestPath = "/employees"
  requestQueryString = {}
  requestHeaders = {}
  requestBody = {}

  requestBody["page_size"] = 1
  requestBody["page_after"] = 3

  result = getEmployees(requestPath, requestQueryString, requestHeaders, requestBody)     
  employees = result["employees"]
  assert len(employees) == 1 , "Cursor test four: The wrong number of employees was returned"
  assert employees[0]["name"] == "Anthony" , "Cursor test four: The wrong second employee was returned"



def testGetEmployees():
  getEmployeesTestOne()
  print("Employee test one passed")
  getEmployeesTestTwo()
  getEmployeesTestThree()
  getEmployeesTestFour()
  print("all employees test passed!")

def postPayrollRunTestOne():
  requestPath = "/payroll-run"
  requestQueryString = {}
  requestHeaders = {}
  requestBody = {}

  requestBody["hours_worked"] = 40

  postPayrollRun(requestPath, requestQueryString, requestHeaders, requestBody)     
  result = executeQuery("select * from payroll_run_employee_payments")
  assert len(result) == 4 , "Wrong number of records in database result"
  assert float(result[0]["amount"]) == 40*10.01 , "David has the wrong amount paid in the pay period for the hours worked"

def testPostPayrollRun():
  postPayrollRunTestOne()

def testPostPayrollRunEmployeePayment():
  pass

if __name__ == "__main__":
    testGetEmployees()
    testPostPayrollRun()

