program pid_controller
  implicit none
  
  real :: setpoint, process_variable, error
  real :: kp, ki, kd, integral, derivative
  real :: previous_error, output
  integer :: iostat
  
  ! File variables
  character(len=50) :: file_name = "pid_data.txt"
  integer, parameter :: unit_number = 10
  
  ! Open the file for reading
  open(unit=unit_number, file=file_name, status='old', action='read', iostat=iostat)
  
  ! Check if file exists and read values if it does
  if (iostat == 0) then
     read(unit_number, *) integral, previous_error
  else
     ! Default values if file doesn't exist
     integral = 0.0
     previous_error = 0.0
  end if
  
  ! Close the file
  close(unit=unit_number)
  
  ! Setpoint, process variable, and PID gains
  setpoint = 50.0
  process_variable = 0.0
  kp = 0.5
  ki = 0.1
  kd = 0.2
  
  ! Main control loop
  do
     ! Calculate error
     error = setpoint - process_variable
     
     ! Update integral term
     integral = integral + error
     
     ! Update derivative term
     derivative = error - previous_error
     
     ! Calculate output
     output = kp * error + ki * integral + kd * derivative
     
     ! Update previous error
     previous_error = error
     
     ! Update process variable (simulate process response)
     process_variable = process_variable + output
     
     ! Print output
     print *, "Output:", output
     
     ! Add delay (simulate process response time)
     call sleep(1)
     
  end do
  
  ! Open the file for writing
  open(unit=unit_number, file=file_name, status='replace', action='write', iostat=iostat)
  
  ! Write integral and previous error values to the file
  write(unit_number, *) integral, previous_error
  
  ! Close the file
  close(unit=unit_number)
  
contains

  subroutine sleep(seconds)
    integer, intent(in) :: seconds
    integer :: i
    do i = 1, 1000000 * seconds
       ! Do nothing, just waste time to simulate delay
    end do
  end subroutine sleep
  
end program pid_controller


