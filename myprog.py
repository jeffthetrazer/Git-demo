from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (replace with database integration)
doctors = [
    {"doctor_id": 1, "name": "Dr. Smith", "specialty": "Cardiologist", "schedule": ["Monday 5:00 PM", "Wednesday 6:30 PM"]},
    # Add more doctors here
]

appointments = []  # Store booked appointments here

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc['doctor_id'] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    return jsonify({"error": "Doctor not found"}), 404

@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    appointment_time = data.get('appointment_time')

    # Check doctor's availability
    doctor = next((doc for doc in doctors if doc['doctor_id'] == doctor_id), None)
    if doctor and appointment_time in doctor['schedule']:
        appointment = {
            "appointment_id": len(appointments) + 1,
            "patient_name": data.get('patient_name'),
            "doctor_id": doctor_id,
            "appointment_time": appointment_time
        }
        appointments.append(appointment)
        return jsonify({"message": "Appointment booked successfully"})
    
    return jsonify({"error": "Doctor not found or appointment slot unavailable"}), 400

if __name__ == '__main__':
    app.run(debug=True)
