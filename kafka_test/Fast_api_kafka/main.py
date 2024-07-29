import logging
from fastapi import FastAPI, HTTPException,status
from models import EmployeesInput, EmployeesResponse
from database import producer, consumer, Topic_name
from kafka import  TopicPartition
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

@app.post("/data/", response_model=EmployeesResponse)
async def create_employee(employee_input: EmployeesInput):
    try:
        producer.send('first', employee_input.dict())
        producer.flush()
        return employee_input
    except Exception as e:
        logging.error(f"Error sending employee data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

'''@app.get("/getdata/{employee_id}", response_model=EmployeesResponse)
async def get_employee(employee_id: int):
    try:
        for message in consumer:
            if message.value['id'] == employee_id:
                employee_response = EmployeesResponse(**message.value)
                return employee_response
            #else:
            #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Error getting employee data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
'''
@app.get("/getdata/{employee_id}", response_model=EmployeesResponse)
async def get_employee(employee_id: int):
    try:
        consumer.seek(TopicPartition(Topic_name, 0), 0)  # Reset consumer to the beginning of the topic
        for message in consumer:
            if message.value['id'] == employee_id:
                employee_response = EmployeesResponse(**message.value)
                return employee_response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    except Exception as e:
        logging.error(f"Error getting employee data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)