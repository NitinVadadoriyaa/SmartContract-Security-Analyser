pragma solidity ^0.8.1;

contract CollegeData {
    
    struct Student{
        uint rollNo;
        string studentName;
        string class;
    }
  Student[] public students;
  uint public netxtStudentRollNo;
  
  function create(string memory name, string memory class) public
  {
      students.push(Student(netxtStudentRollNo, name, class));
      netxtStudentRollNo++;
  }
  
  function read(uint studentRollNo ) view public returns(uint, string memory, string memory)
  {
      if(studentRollNo < students.length && studentRollNo>= 0)
      {
          return(students[studentRollNo].rollNo, students[studentRollNo].studentName, students[studentRollNo].class);
      }
      revert("Student doesn't exist");
  }
  function update(uint studentRollNo, string memory studentName, string memory studentClass) public
  {
       if(studentRollNo < students.length && studentRollNo>= 0)
      {
          students[studentRollNo].studentName  = studentName;
          students[studentRollNo].class = studentClass;
      }

  }
  function destroy(uint studentRollNo) public
  {
       if(studentRollNo < students.length && studentRollNo>= 0)
      {
         delete students[studentRollNo];
      }
  }

}
