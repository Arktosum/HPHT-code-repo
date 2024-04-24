program pid_controller
  implicit none
  
  real :: setpoint, process_variable, error
  real :: kp, ki, kd, integral, derivative
  real :: previous_error, output
  
  ! Setpoint, process variable, and PID gains
  setpoint = 50.0
  process_variable = 0.0
  kp = 0.5
  ki = 0.1
  kd = 0.2
  
  ! Initialize integral and derivative terms
  integral = 0.0
  previous_error = 0.0
  
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
  
contains

  subroutine sleep(seconds)
    real, intent(in) :: seconds
    integer :: i
    do i = 1, 1000000 * seconds
       ! Do nothing, just waste time to simulate delay
    end do
  end subroutine sleep
  
end program pid_controller
