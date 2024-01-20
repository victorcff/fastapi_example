from fastapi import FastAPI, Path
from typing import Annotated, Optional
from pydantic import BaseModel

app = FastAPI()

students = {
  1: {
    "name": "carlos",
    "age": 23,
    "class": "2012"
  }
}

class Student(BaseModel):
  name: str
  age: int
  year: str
  
class UpdateStudent(BaseModel):
  name: Optional[str] = None
  age: Optional[int] = None
  year: Optional[str] = None

@app.get("/")
async def Home():
  return "Welcome Home"

@app.get("/get_students", summary="Get all students")
def get_students():
  return students

@app.get("/get-student/{student_id}", summary="Get student by ID")
def get_student(student_id: Annotated[int, Path(description="The ID of the student you want to view", gt=0, lt=3)]):
  return(students[student_id])

@app.get("/get-student-by-name", summary="Get student by name")
def get_student(*, name: Optional[str] = None, id: int):
  for student_id in students:
    if students[student_id]["name"] == name:
      return students[student_id]
    return {"Data": "Not found"}
  
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
  if student_id in students:
    return {"Error": "Student already exists"}
  students[student_id] = student
  return students[student_id]

@app.put("/update-student{student_id}")
def update_student(student_id: int, student: UpdateStudent):
  if student_id not in students:
    return {"Error": "Student does not exist"}
  if student.name != None:
    students[student_id].name = student.name
  if student.age != None:
    students[student_id].age = student.age
  if student.year != None:
    students[student_id].year = student.year
  return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
  if student_id not in students:
    return {"Error": "Student does not exist"}
  del students[student_id]
  return {"Message": "Student deleted succesfully"}