from flask import Flask, redirect, request,jsonify,abort

app = Flask(__name__)
data_file = "data.csv"
employees = []

@app.route('/')
def hello():
    hostname = request.headers.get('Host')
    return f"Port address :{hostname}"
@app.route('/version')


# Helper function to read data from the CSV file
def read_data():
    try:
        with open(data_file, "r") as file:
            data = [line.strip().split(",") for line in file.readlines()]
            return [{"id": row[0], "name": row[1], "age": row[2],"address":row[3],"is_active":row[4]} for row in data]
    except FileNotFoundError:
        return jsonify("Error while accessing data resource"),500

# Helper function to write data to the CSV file
def write_data(data):
    with open(data_file, "w") as file:
        for employee in data:
            file.write(f"{employee['id']},{employee['name']},{employee['age']},{employee['address']},{employee['is_active']}\n")

@app.route('/employees', methods=['POST'])
def create_employee():
    req_data = request.get_json()

    if 'name' not in req_data or 'address' not in req_data or 'age' not in req_data:
        return "Invalid Json Format",400
    for employee in employees:
        if employee['name']==req_data['name']:
            return "Data resource already exists. Use PUT to update data",409
    is_active=True
    if 'is_active' in req_data:
        is_active=req_data['is_active']
    new_employee = {
        "id": str(len(employees) + 1),  
        "name": req_data['name'],
        "age":req_data['age'],
        "address": req_data['address'],
        "is_active":is_active
    }

    employees.append(new_employee)
    write_data(employees)

    return f"{(new_employee)},Data resource created successfully", 200

@app.route('/employees', methods=['GET'])
def get_employees_based_on_active_state():
    try:
        is_active=None
        is_active=request.args.get('is_active')
        if is_active==None:
            return jsonify(employees),200
        active_employee=[]    
        for e in employees:
            if e['is_active']==is_active:
                active_employee.append(e)        
        return jsonify(active_employee),200
    except:
        return jsonify("Error while accessing data resource"),500
# Retrieve (GET) endpoint
@app.route('/employees/<employee_name>', methods=['GET'])
def get_employee_with_name(employee_name):
    employee = next((employee for employee in employees if employee['name'] == employee_name), None)
    if employee is None:
        return jsonify("Data resource not created"),404  # Not Found
    return jsonify(employee),200

# Update (PUT) endpoint
@app.route('/employees/<employee_name>', methods=['PUT'])
def put_employee(employee_name):
    req_data = request.get_json()

    if 'name' not in req_data or 'address' not in req_data or 'age' not in req_data:
        return "Invalid Json Format",400
    
    global employees
    for employee in employees:
        if  employee['name']==employee_name:
            employee['name']=req_data['name']
            employee['age']=req_data['age']
            employee['address']=req_data['address']
            employee['is_active']=req_data['is_active'] if 'is_active' in req_data else employee['is_active']
            write_data(employees)
            return jsonify("Data resource update successfully"), 200
    return jsonify("Data resource not created"),404
    
# Delete (DELETE) endpoint
@app.route('/employees/<employee_name>', methods=['DELETE'])
def delete_employee(employee_name):
    global employees
    employees = [employee for employee in employees if employee['name'] != employee_name]
    write_data(employees)
    
    return 'employee deleted successfully', 200

def new_route():
    response_data="Hi there!"
    return jsonify(response_data),200
@app.errorhandler(404)
def not_found(error):
    return "Page not Found",404

if __name__ == '__main__':
    employees = read_data()
    app.run(debug=True,port=9090)
